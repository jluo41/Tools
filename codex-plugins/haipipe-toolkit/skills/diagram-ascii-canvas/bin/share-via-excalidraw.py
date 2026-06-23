#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright"]
# ///
"""Upload a .excalidraw to excalidraw.com via drag-drop → return shareable link."""
from __future__ import annotations

import asyncio, base64, json, re, sys
from pathlib import Path
from playwright.async_api import async_playwright

DEBUG = Path("/tmp/excalidraw_share_debug")
DEBUG.mkdir(exist_ok=True)


async def shot(page, name):
    p = DEBUG / f"{name}.png"
    await page.screenshot(path=p)
    print(f"  📸 {p}", flush=True)


async def list_buttons(page):
    return await page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('button, [role="button"], a').forEach(b => {
            const r = b.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) return;
            out.push({
                tag: b.tagName,
                aria: b.getAttribute('aria-label'),
                title: b.getAttribute('title'),
                text: (b.innerText || '').trim().slice(0, 80),
                cls: (b.className || '').toString().slice(0, 100),
            });
        });
        return out;
    }""")


async def main(file_path: str):
    f = Path(file_path).resolve()
    print(f"📂 file: {f}  ({f.stat().st_size:,} bytes)", flush=True)
    b64 = base64.b64encode(f.read_bytes()).decode()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1600, "height": 1000})
        page = await ctx.new_page()
        page.set_default_timeout(30_000)

        print("🌐 loading excalidraw.com ...", flush=True)
        await page.goto("https://excalidraw.com/", wait_until="domcontentloaded")
        await page.wait_for_selector("canvas", timeout=30_000)
        await page.wait_for_timeout(2_500)
        await shot(page, "01_loaded")

        # Inject the file via a synthetic drop event on the canvas / body
        print("📁 dropping file via DataTransfer ...", flush=True)
        result = await page.evaluate("""async (args) => {
            const bytes = Uint8Array.from(atob(args.b64), c => c.charCodeAt(0));
            const file = new File([bytes], args.name, { type: 'application/json' });
            const dt = new DataTransfer();
            dt.items.add(file);
            // Pick the most likely target
            const canvas = document.querySelector('canvas');
            const target = canvas || document.body;
            const rect = target.getBoundingClientRect();
            const cx = rect.left + rect.width / 2;
            const cy = rect.top + rect.height / 2;
            // Fire the full sequence: dragenter → dragover → drop
            for (const type of ['dragenter', 'dragover', 'drop']) {
                const ev = new DragEvent(type, {
                    bubbles: true, cancelable: true, composed: true,
                    dataTransfer: dt, clientX: cx, clientY: cy,
                });
                target.dispatchEvent(ev);
            }
            return { target: target.tagName, x: cx, y: cy };
        }""", {"b64": b64, "name": f.name})
        print(f"  → drop dispatched on {result}", flush=True)
        await page.wait_for_timeout(4_000)
        await shot(page, "02_after_drop")

        # Verify scene loaded — Excalidraw stores element count in window
        loaded_count = await page.evaluate("""() => {
            // Check if canvas has any drawn content (rough heuristic)
            const c = document.querySelector('canvas');
            if (!c) return 0;
            // Better: inspect localStorage
            const s = localStorage.getItem('excalidraw');
            if (s) try { return JSON.parse(s).length; } catch { return -1; }
            return -2;
        }""")
        print(f"  scene element count (via localStorage): {loaded_count}", flush=True)

        if loaded_count is None or loaded_count == 0 or loaded_count == -2:
            # Drop didn't take. Try alternate: dispatch on the App container
            print("  drop may have failed — trying alternate target ...", flush=True)
            await page.evaluate("""async (args) => {
                const bytes = Uint8Array.from(atob(args.b64), c => c.charCodeAt(0));
                const file = new File([bytes], args.name, { type: 'application/json' });
                const dt = new DataTransfer();
                dt.items.add(file);
                const target = document.querySelector('.excalidraw') ||
                               document.querySelector('.excalidraw-container') ||
                               document.body;
                const r = target.getBoundingClientRect();
                for (const type of ['dragenter', 'dragover', 'drop']) {
                    target.dispatchEvent(new DragEvent(type, {
                        bubbles: true, cancelable: true, composed: true,
                        dataTransfer: dt,
                        clientX: r.left + r.width/2,
                        clientY: r.top + r.height/2,
                    }));
                }
            }""", {"b64": b64, "name": f.name})
            await page.wait_for_timeout(4_000)
            await shot(page, "02b_after_drop_retry")
            loaded_count = await page.evaluate("""() => {
                const s = localStorage.getItem('excalidraw');
                if (s) try { return JSON.parse(s).length; } catch { return -1; }
                return -2;
            }""")
            print(f"  retry scene count: {loaded_count}", flush=True)

        # Confirm any "load existing scene" dialog
        for label in ["Load", "Replace", "Confirm", "Yes", "OK"]:
            btn = page.locator(f'button:has-text("{label}")').first
            if await btn.count() > 0 and await btn.is_visible():
                try:
                    await btn.click(timeout=2_000)
                    print(f"  → dismissed dialog: {label}", flush=True)
                    await page.wait_for_timeout(1_000)
                except Exception:
                    pass

        await shot(page, "03_pre_share")

        # Click Share
        print("🔗 clicking Share button ...", flush=True)
        share = page.locator(".collab-button").first
        await share.wait_for(state="visible")
        await share.click()
        await page.wait_for_timeout(2_500)
        await shot(page, "04_share_dialog")

        btns = await list_buttons(page)
        DEBUG.joinpath("04_share_buttons.json").write_text(json.dumps(btns, indent=2))

        # Find shareable-link control
        link_labels = [
            "Export to Link", "Export to link",
            "Shareable link", "Shareable Link",
            "Get shareable link", "Create shareable link",
            "Export", "Generate link",
        ]
        clicked_label = None
        for label in link_labels:
            loc = page.locator(f'button:has-text("{label}")').first
            if await loc.count() > 0 and await loc.is_visible():
                clicked_label = label
                print(f"  ✓ clicking: '{label}'", flush=True)
                await loc.click()
                break
        if not clicked_label:
            print("  no shareable-link button found — see 04_share_buttons.json", file=sys.stderr)
            await browser.close()
            return 3

        await page.wait_for_timeout(4_000)
        await shot(page, "05_link_generated")

        # Extract URL
        url = None
        body_text = await page.locator("body").inner_text()
        m = re.search(r"https://excalidraw\.com/#json=[\w=,+/-]+", body_text)
        if m: url = m.group(0)
        if not url:
            inputs = page.locator("input")
            for i in range(await inputs.count()):
                v = await inputs.nth(i).input_value()
                if v and "excalidraw.com/#json=" in v:
                    url = v
                    break

        if not url:
            btns2 = await list_buttons(page)
            DEBUG.joinpath("05_after_link_buttons.json").write_text(json.dumps(btns2, indent=2))
            print("✗ URL not extracted; inspect /tmp/excalidraw_share_debug/", file=sys.stderr)
            await browser.close()
            return 4

        print(f"\n✅ {url}\n", flush=True)
        data = json.loads(f.read_text())
        data["shareUrl"] = url
        f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"📝 shareUrl written into {f}", flush=True)
        await browser.close()
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv[1])))
