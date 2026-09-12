"""Sentence-addressed SHAPE review, presented below each paragraph."""
import datetime as dt
import html
import re

from live.outline_preview import (
    page_lock, preview_path, read_previews, record_token, bullet_token,
    write_previews, reader_prose,
)
from src.outline_version import latest_outline
from src.plan_shape import iter_plan_bullets


def comments(record):
    result = []
    for raw in re.split(r"(?m)(?=^> Comment )", record.get("reviews", "")):
        if not raw.strip():
            continue
        match = re.match(r"> Comment (.+?) · \[(PC[a-f0-9]{32})\] (.*?) · (\d{6} \d{4} UTC)\n", raw + "\n")
        if not match:
            # Hand-authored/legacy review remains visible rather than discarded.
            result.append({"raw": raw.strip(), "status": "Open"})
            continue
        quote = re.search(r"(?m)^> Quote: (.*)$", raw)
        shape = re.search(r"(?m)^> Shape: (.*)$", raw)
        replies = re.findall(r"(?m)^>> (.*)$", raw)
        result.append({"id": match[2], "author": match[1], "text": match[3],
                       "date": match[4], "quote": quote[1] if quote else "",
                       "shape": shape[1] if shape else "", "replies": replies,
                       "status": "Addressed" if any(" · Addressed:" in r for r in replies) else "Open"})
    return result


def comment_list(records, paragraph):
    out, open_count = [], 0
    esc = html.escape
    for address, record in records.items():
        if address.rsplit(".", 1)[0] != paragraph:
            continue
        for item in comments(record):
            open_count += item["status"] == "Open"
            if "raw" in item:
                out.append('<article class="preview-comment"><strong>%s · Open</strong><pre>%s</pre></article>' %
                           (esc(address), esc(item["raw"])))
                continue
            changed = item["quote"] != record["text"]
            out.append('<article class="preview-comment" id="%s"><header><strong>%s · %s</strong>'
                       '<span>%s · %s</span></header><blockquote>%s</blockquote><p>%s</p>%s%s</article>' % (
                           esc(item["id"]), esc(address), item["status"], esc(item["author"]), esc(item["date"]),
                           esc(reader_prose(item["quote"])), esc(item["text"]),
                           '<small>Sentence revised since this comment</small>' if changed else '',
                           ''.join('<p class="comment-reply">%s</p>' % esc(reply) for reply in item["replies"])))
    return ''.join(out), open_count


def paragraph_comments(records, blocks, paragraph, path_q, file_q):
    options = []
    esc = html.escape
    for address, block in blocks.items():
        if block["paragraph"] != paragraph:
            continue
        record = records.get(address)
        prose = reader_prose(record["text"]) if record else ''
        options.append('<option value="%s"%s>%s · %s</option>' % (
            esc(address), '' if prose else ' disabled', esc(address),
            esc(prose[:100] + ('…' if len(prose) > 100 else '') if prose else 'No saved draft yet')))
    listing, count = comment_list(records, paragraph)
    return ('<details class="paragraph-comments"><summary>Comments · <span data-comment-count>%s</span></summary>'
            '<div data-comment-list>%s</div><form data-preview-comment>'
            '<input type="hidden" name="path" value="%s"><input type="hidden" name="file" value="%s">'
            '<label>Sentence<select name="address" required><option value="">Choose a sentence…</option>%s</select></label>'
            '<blockquote data-comment-quote hidden></blockquote>'
            '<label>Your name<input name="author" autocomplete="name" maxlength="80" required></label>'
            '<label>Comment<textarea name="comment" rows="3" maxlength="8000" required '
            'placeholder="What should change in this sentence?"></textarea></label>'
            '<button type="submit">Save comment</button> <span role="status" data-comment-status></span>'
            '<small>Saved for review. Ask your agent to apply comments; saving does not start it.</small>'
            '</form></details>') % (comment_summary(records, paragraph), listing,
                                    esc(path_q or ''), esc(file_q or ''), ''.join(options))


def comment_summary(records, paragraph):
    statuses = [item['status'] for address, record in records.items()
                if address.rsplit('.', 1)[0] == paragraph for item in comments(record)]
    if not statuses:
        return 'Add comment'
    return '%d open · %d addressed' % (statuses.count('Open'), statuses.count('Addressed'))


def save_comment(page, payload):
    """Append once, with exact saved-sentence and Bullet checks; never publish."""
    address, identity = payload.get("address"), payload.get("comment_id")
    if not isinstance(address, str) or not re.fullmatch(r"C\d+\.P\d+\.B\d+", address):
        return None, "Choose a sentence"
    if not isinstance(identity, str) or not re.fullmatch(r"PC[a-f0-9]{32}", identity):
        return None, "Missing comment identity; reopen the comment form"
    for field, limit in (("author", 80), ("comment", 8000)):
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            return None, "%s is required (maximum %d characters)" % (field.capitalize(), limit)
    author = ' '.join(payload['author'].split())
    message = ' '.join(payload['comment'].split())
    if '·' in author:
        return None, "Use a name without the middle-dot separator"
    with page_lock(page):
        path = preview_path(page)
        if path.is_symlink() or path.parent.is_symlink():
            return None, "Preview source must be local Markdown"
        records = read_previews(page)
        record = records.get(address)
        # Lost-response retries are idempotent even if prose subsequently changed.
        for other_address, other_record in records.items():
            for item in comments(other_record):
                if item.get('id') != identity:
                    continue
                if (other_address, item.get('author'), item.get('text')) != (address, author, message):
                    return None, "Comment identity already belongs to another comment"
                listing, count = comment_list(records, address.rsplit('.', 1)[0])
                return {"comment_id": identity, "comments_html": listing, "open_count": count,
                        "summary": comment_summary(records, address.rsplit('.', 1)[0])}, None
        if not record or not record['text']:
            return None, "Save a candidate sentence before commenting"
        plan = latest_outline(page.parent / 'outline', page.stem)
        blocks = {b['address']: b for b in iter_plan_bullets(plan.read_text())} if plan else {}
        if address not in blocks or payload.get('expected_bullet') != bullet_token(blocks[address]):
            return None, "Bullet changed; reload and review before commenting"
        if payload.get('expected_record') != record_token(record):
            return None, "Sentence changed; reload and review before commenting"
        date = dt.datetime.now(dt.timezone.utc).strftime('%y%m%d %H%M UTC')
        lane = '> Comment %s · [%s] %s · %s\n> Quote: %s\n> Shape: %s' % (
            author, identity, message, date, record['text'], record['plan'])
        record['reviews'] = (record.get('reviews', '').rstrip() + '\n\n' + lane).strip()
        write_previews(page, records)
        listing, count = comment_list(records, address.rsplit('.', 1)[0])
        return {"comment_id": identity, "comments_html": listing, "open_count": count,
                "summary": comment_summary(records, address.rsplit('.', 1)[0])}, None
