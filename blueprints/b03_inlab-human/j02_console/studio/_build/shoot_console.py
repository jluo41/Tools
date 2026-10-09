"""Shoot the In-Lab Console on its SYNTHETIC fixtures, for the j02 studio topics (s11 s12 s13 s21 s32).

The console must be running on the fixtures only (`bash Tools/plugins/inlab-human/servers/haichat-inlab/fixtures/
run_fixture.sh`, which prints its PIDs). This script refuses a console whose datasets are not the synthetic ones,
so no real patient is ever on screen. It writes:

    s12-individual-scope/shots/<view>.png      every view, Individual scope, a synthetic glucose human
    s11-group-scope/shots/<view>.png           every view, Group scope
    s13-case-builder/shots/case_<dataset>.png  the Case view on each of the three data types
    s21-run-bar/shots/run_<model>.png          the Model view after ▶ Run, for both stub endpoints
    s32-console-element-ui/shots/<el>.png      one crop per element, and facts.json (each one's computed style)
    s32-console-element-ui/shots/approval.png  the HaiChat drawer with an Allow/Deny card, when the agent answers

    uv run --with playwright python shoot_console.py [--base http://127.0.0.1:8191] [--no-agent]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent
sys.path.insert(0, str(STUDIO.parents[2] / "_build"))
from shoot import browser, page_shot, snap  # noqa: E402
from console_draw import HIDDEN  # noqa: E402  — views a scope hides (views.ts PLACEHOLDER, j02 Q05)

VIEWS = ["Raw", "Source", "Record", "Case", "Internal", "External", "Model", "Tasks", "Checklist", "Annotate",
         "Health"]
SYNTHETIC = {"SynthCGM_v0", "SynthDialogue_v0", "SynthReview_v0"}
FIRST = {"SynthCGM_v0": "synth-cgm-001", "SynthDialogue_v0": "synth-dlg-001", "SynthReview_v0": "synth-phy-001"}

# (key, what it is, the selector, the view it is shot on; "" = whatever is open)
ELEMENTS = [
    ("topbar", "Top bar", ".topbar", ""),
    ("scope-toggle", "Scope toggle (Individual · Group)", ".level-toggle", ""),
    ("dataset-picker", "Dataset picker", ".ds-picker", ""),
    ("patient-picker", "Patient picker, open", ".combo", "@combo"),
    ("haichat-toggle", "HaiChat toggle", ".chat-toggle", ""),
    ("nav-rail", "Nav rail (Data · Insight · Action · Health)", ".navrail", ""),
    ("tab-strip", "Tab strip", ".tabstrip", "Source"),
    ("patient-card", "Patient card", ".patient-card", "Source"),
    ("layer-banner", "Layer banner (store and transform)", ".layer-banner", "Source"),
    ("source-table", "Source table (tabs, grid, as-of)", ".raw", "Source"),
    ("raw-file", "Raw file preview", ".raw-file", "Raw"),
    ("record-chart", "Record chart (a lane per table with a time column)", ".record-chart", "Record"),
    ("case-card", "Case card", ".case-card", "Case"),
    ("model-list", "Model list", ".mv-side", "Model"),
    ("model-card", "Model card", ".mv-body", "Model"),
    ("run-bar", "Run bar (Run · Interpret · Message · Judge · Feedback)", ".pipe-bar", "@run"),
    ("forecast-chart", "Forecast chart (context · forecast · observed)", ".fc", "@run"),
    ("runs-table", "Runs table", ".runs-table", "@run"),
    ("checklist-bar", "Checklist bar", ".cl-bar", "Checklist"),
    ("annotate-start", "Annotate start (Group)", ".fg-start", "@group:Annotate"),
    ("health-table", "Health table", ".health-table", "Health"),
    ("drawer", "HaiChat drawer", ".drawer", "@drawer"),
    ("refused", "HaiChat tool call the gate refused", ".tc-chip.refused", "@refusals"),
]
# (dropped 261009: the Internal chart and the placeholder card, whose views are hidden as placeholders, j02 Q05)


# a screenshot never carries a host path: any home-folder path on screen (the Health view prints the
# resolved stores) is shown as <SPACE>/… before the shot (AGENTS.md rule 7; nothing in Tools names one machine)
MASK_JS = r"""() => { const re = /\/(?:Users|home|private)\/[^\s"']*?\/(?=Tools\/)/g;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) { if (re.test(n.nodeValue)) n.nodeValue = n.nodeValue.replace(re, '<SPACE>/'); re.lastIndex = 0; } }"""


def masked(page) -> None:
    page.evaluate(MASK_JS)


def shown(views: list[str], scope: str) -> list[str]:
    """The views the rail lists at a scope: a placeholder there is hidden (j02 Q05)."""
    return [v for v in views if scope not in HIDDEN.get(v.lower(), [])]


READY = "() => { const b = document.querySelector('.drawer-input .send'); return b && !b.disabled; }"
REFUSED = "(t) => [...document.querySelectorAll('.tc-chip.refused')].some(c => c.innerText.includes(t))"


def refusals(page, box, element) -> dict:
    """The gate's two refusals, as the drawer shows them (j02 g02 D5): Deny on the approval card ("declined"),
    and a tool in neither list ("not permitted", prepare_payload). Each must leave a chip marked refused,
    never one that looks as if it ran. The agent often tries prepare_payload on its own; asked only if not."""
    out = {}
    page.locator(".appr-card button", has_text="Deny").first.click()
    for key, text, ask in (("declined", "declined", None),
                           ("not_permitted", "not permitted",
                            "Call the tool mcp__endpoint-predict__prepare_payload with patient_id synth-cgm-001 and "
                            "model synth_cgm_forecast_v0001, and tell me what happened.")):
        try:
            if ask and not page.evaluate(REFUSED, text):
                page.wait_for_function(READY, timeout=180000)       # the turn before must be over
                box.fill(ask)
                box.press("Enter")
            page.wait_for_function(REFUSED, arg=text, timeout=120000)
            chip = page.locator(".tc-chip.refused", has_text=text).first
            out[key] = chip.inner_text().replace("\n", " ")
            if key == "not_permitted":
                chip.scroll_into_view_if_needed()
                chip.evaluate("c => c.dataset.shot = 'refused'")         # so the element helper can find it
                element("refused", "HaiChat tool call the gate refused", ".tc-chip[data-shot='refused']")
        except Exception as e:  # noqa: BLE001 — say what did not happen; the drawing marks it red
            out[key] = f"no '{text}' chip within the wait ({type(e).__name__})"
    page.wait_for_function(READY, timeout=180000)
    page.wait_for_timeout(800)
    masked(page)
    page_shot(page, STUDIO / "s32-console-element-ui" / "shots" / "refused_page.png")
    return out


def select(page, dataset: str, human: str) -> None:
    page.select_option("select.ds-select", dataset)
    page.wait_for_timeout(800)
    page.click(".combo-btn")
    page.wait_for_timeout(400)
    page.get_by_text(human).first.click()
    page.wait_for_timeout(1500)


def view(page, name: str) -> None:
    page.locator(".nr-item", has_text=name).first.click()
    page.wait_for_timeout(1400)


def scope(page, which: str) -> None:
    page.locator(".level-toggle button", has_text=which).first.click()
    page.wait_for_timeout(1200)


def run(page, model_hint: str) -> None:
    view(page, "Model")
    page.locator(".roster-item", has_text=model_hint).first.click()
    page.wait_for_timeout(600)
    page.locator(".mv-tab", has_text="Run").first.click()
    page.wait_for_timeout(600)
    page.locator(".mv-body button", has_text="Run").first.click()
    page.wait_for_timeout(3500)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8191")
    ap.add_argument("--no-agent", action="store_true", help="skip the approval card (no agent turn)")
    a = ap.parse_args()
    shots = {t: STUDIO / t / "shots" for t in ("s11-group-scope", "s12-individual-scope", "s13-case-builder",
                                                "s21-run-bar", "s32-console-element-ui")}
    for d in shots.values():
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.png"):
            old.unlink()
    facts: dict = {}
    with browser() as page:
        page.goto(a.base + "/")
        page.wait_for_selector("select.ds-select option", state="attached", timeout=30000)
        page.wait_for_timeout(1000)
        offered = set(page.eval_on_selector_all("select.ds-select option", "os => os.map(o => o.value)"))
        if not offered or not offered <= SYNTHETIC:
            sys.exit(f"refusing to shoot: the console offers {sorted(offered)}, not only the synthetic fixtures")

        def element(key: str, label: str, sel: str) -> None:
            masked(page)
            got = snap(page, sel, shots["s32-console-element-ui"] / f"{key}.png")
            facts[key] = {"label": label, **(got or {"selector": sel, "missing": True})}

        # Individual scope, the synthetic glucose human: every view, and the elements each shows
        select(page, "SynthCGM_v0", FIRST["SynthCGM_v0"])
        for key, label, sel, on in ELEMENTS:
            if on == "":
                element(key, label, sel)
        page.click(".combo-btn")
        page.wait_for_timeout(400)
        element("patient-picker", "Patient picker, open", ".combo")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        for v in shown(VIEWS, "individual"):
            view(page, v)
            masked(page)
            page_shot(page, shots["s12-individual-scope"] / f"{v.lower()}.png")
            for key, label, sel, on in ELEMENTS:
                if on == v:
                    element(key, label, sel)
        # the run bar, on both stub endpoints
        run(page, "cgm")
        page_shot(page, shots["s21-run-bar"] / "run_cgm_forecast.png")
        for key, label, sel, on in ELEMENTS:
            if on == "@run":
                element(key, label, sel)
        # the Case view on each data type
        for ds, human in FIRST.items():
            select(page, ds, human)
            view(page, "Case")
            page_shot(page, shots["s13-case-builder"] / f"case_{ds}.png")
        select(page, "SynthDialogue_v0", FIRST["SynthDialogue_v0"])
        run(page, "risk")
        page_shot(page, shots["s21-run-bar"] / "run_risk_score.png")
        # Group scope: every view
        scope(page, "Group")
        for v in shown(VIEWS, "group"):
            view(page, v)
            masked(page)
            page_shot(page, shots["s11-group-scope"] / f"{v.lower()}.png")
            if v == "Annotate":
                element("annotate-start", "Annotate start (Group)", ".fg-start")
        scope(page, "Individual")
        # the HaiChat drawer, and (one agent turn on synthetic data) its Allow/Deny card
        select(page, "SynthCGM_v0", FIRST["SynthCGM_v0"])
        page.click(".chat-toggle")
        page.wait_for_timeout(2500)
        element("drawer", "HaiChat drawer", ".drawer")
        status = "skipped (--no-agent)"
        if not a.no_agent:
            box = page.locator(".drawer-input input, .drawer-input textarea").first
            if box.is_enabled():
                box.fill("Please run the selected glucose model on this patient.")
                box.press("Enter")
                try:
                    page.wait_for_selector(".appr-card", timeout=120000)
                    page.wait_for_timeout(500)
                    element("approval", "HaiChat approval card (Allow · Deny)", ".appr-card")
                    page_shot(page, shots["s32-console-element-ui"] / "approval_page.png")
                    status = "shot"
                    facts["_refused"] = refusals(page, box, element)
                except Exception as e:  # noqa: BLE001 — no card in time: say so, the drawing marks it red
                    status = f"no approval card within 120 s ({type(e).__name__})"
            else:
                status = "the agent is offline (its input is disabled)"
        facts["_approval"] = status
    (shots["s32-console-element-ui"] / "facts.json").write_text(json.dumps(facts, indent=1), encoding="utf-8")
    missing = [k for k, v in facts.items() if isinstance(v, dict) and v.get("missing")]
    print(f"shot {sum(len(list(d.glob('*.png'))) for d in shots.values())} images; elements missing: {missing}; "
          f"approval card: {status}")


if __name__ == "__main__":
    main()
