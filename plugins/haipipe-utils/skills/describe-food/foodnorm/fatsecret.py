"""
FatSecret Platform API, used live: search a food name, pick the result whose words agree, read its servings.

    from foodnorm import fatsecret as fs
    hit, share = fs.pick("Keto Bagel Thins (Thomas')", fs.search("Keto Bagel Thins Thomas"))
    food = fs.servings(hit["food_id"])      # name, brand, servings: description, grams, carbs, calories ...

REST API, OAuth 1.0 signed (HMAC-SHA1), so no IP whitelist is needed. The keys come from the environment only:
FATSECRET_CONSUMER_KEY and FATSECRET_CONSUMER_SECRET (env.sh loads them from ~/.fatsecret.env). The free Basic plan
allows 5,000 calls a day and US foods; asked too fast it answers error 12, and call() waits and asks again, as it
does when the network drops (5 s, then longer, about 8 minutes in all).

Its terms let only ids (food_id, serving_id) be stored past 24 hours. Names and numbers read here are for use now:
a caller keeps the ids and fetches the numbers again when it needs them.
"""
import base64
import hashlib
import hmac
import os
import re
import time
import urllib.parse as up
import uuid
from typing import Dict, List, Optional, Tuple

import requests

URL = "https://platform.fatsecret.com/rest/server.api"
SKIP = {"a", "an", "and", "with", "of", "the", "in", "on", "or", "to", "for", "g", "ml", "oz", "piece", "pieces",
        "bag", "bowl", "bowls", "cup", "cups", "plate", "slice", "slices", "small", "large", "medium"}
WAITS = (5, 15, 30, 60, 120, 240)                          # seconds to wait on error 12, then give up


def call(method: str, **params) -> Dict:
    """One signed call; the answer as JSON. Error 12 (too many actions) waits and asks again; other errors return."""
    q = lambda s: up.quote(str(s), safe="-._~")
    for wait in WAITS + (0,):
        p = {**{k: str(v) for k, v in params.items()}, "method": method, "format": "json",
             "oauth_consumer_key": os.environ["FATSECRET_CONSUMER_KEY"], "oauth_nonce": uuid.uuid4().hex,
             "oauth_signature_method": "HMAC-SHA1", "oauth_timestamp": str(int(time.time())), "oauth_version": "1.0"}
        base = "&".join(["GET", q(URL), q("&".join(f"{q(k)}={q(v)}" for k, v in sorted(p.items())))])
        key = (q(os.environ["FATSECRET_CONSUMER_SECRET"]) + "&").encode()
        p["oauth_signature"] = base64.b64encode(hmac.new(key, base.encode(), hashlib.sha1).digest()).decode()
        try:
            ans = requests.get(URL, params=p, timeout=30).json()
        except (requests.RequestException, ValueError):          # the network or a half answer: wait, ask again
            if not wait:
                raise
            time.sleep(wait)
            continue
        if (ans.get("error") or {}).get("code") != 12 or not wait:
            return ans
        time.sleep(wait)
    return ans


def listed(x) -> List:
    """FatSecret writes one result as a bare object and several as a list."""
    return [] if not x else [x] if isinstance(x, dict) else list(x)


def search(text: str, n: int = 10) -> List[Dict]:
    """foods.search: the first n foods, each {food_id, food_name, brand_name?, food_type, food_description}."""
    text = " ".join(re.sub(r"[+&/,()]", " ", str(text)).split())
    return listed(((call("foods.search", search_expression=text, max_results=n) or {}).get("foods") or {}).get("food"))


def words(s) -> List[str]:
    return [w for w in re.findall(r"[a-z]+", str(s).lower()) if w not in SKIP]


def found(w: str, hit_words: List[str]) -> bool:
    """A word is found when it, without a final s, sits inside the result's words joined; under 4 letters, whole."""
    stem = w[:-1] if w.endswith("s") and len(w) > 3 else w
    if len(stem) < 4:
        return stem in hit_words or w in hit_words
    return stem in "".join(hit_words)


def pick(name: str, hits: List[Dict]) -> Tuple[Optional[Dict], float]:
    """The result whose brand and food name hold the most of the name's words, first on a tie; with that share."""
    mine = words(name) or [str(name).lower()]
    best, share = None, 0.0
    for h in hits:
        s = sum(found(w, words(f"{h.get('brand_name', '')} {h['food_name']}")) for w in mine) / len(mine)
        if s > share:
            best, share = h, s
    return best, share


def num(v) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def servings(food_id) -> Optional[Dict]:
    """food.get.v2: {food_id, name, brand, servings: [{serving_id, description, grams, default, carbs, calories,
    protein, fat, fiber, sugar}]}; grams is None when FatSecret gives the serving no metric weight in g."""
    f = (call("food.get.v2", food_id=food_id) or {}).get("food")
    if not f:
        return None
    out = []
    for s in listed((f.get("servings") or {}).get("serving")):
        g = num(s.get("metric_serving_amount")) if s.get("metric_serving_unit") == "g" else None
        out.append({"serving_id": s.get("serving_id"), "description": s.get("serving_description"), "grams": g,
                    "default": s.get("is_default") == "1",
                    **{k: num(s.get(c)) for k, c in (("carbs", "carbohydrate"), ("calories", "calories"),
                                                      ("protein", "protein"), ("fat", "fat"), ("fiber", "fiber"),
                                                      ("sugar", "sugar"))}})
    return {"food_id": f.get("food_id"), "name": f.get("food_name"), "brand": f.get("brand_name"), "servings": out}
