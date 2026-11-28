"""delivery_words.py: are the words a printed Section carries its current words? build_delivery.py runs this file
inside its own namespace (_load_part), so `re` and `Path` come from there.

- stale_message: the stop line when a fragment is older than its page (0.14.0).
- unadopted: a Section whose Page ## Content holds no tagged sentence while it has a Draft (LLMRecJamaAI 261122:
  t02, t04 and t21 printed 28 words each from the placeholder, beside drafts of 2,300 to 8,000 words, and the build
  said DRAFT with no warning). The fix is `page.py adopt <Section folder>`, then export, then build."""

TAGGED = re.compile(r"<!-- realizes: C\d+\.P\d+\.B\d+[a-z]* -->")


def stale_message(lines):
    fix = ("re-export each Section through its LaTeX lane (page.py export <Section folder> --lane latex, "
           "or Delivery > LaTeX rebuild); when a drop is intended, delivery/build.py --accept-dropped-keys "
           "re-exports the stale Sections with md2tex's --accept-dropped-keys and then builds")
    return "\n".join([f"❌ build stopped: {len(lines)} printed Section(s) would carry OLD words"]
                     + [f"  {l}" for l in lines]
                     + [f"  fix: {fix}", "  or build anyway: delivery/build.py --allow-stale (DRAFT, each listed as a G4 blocker)"])


def unadopted(folder, pid):
    """One line when the Section's Content was never adopted from its newest Draft, else []."""
    face, drafts = Path(folder) / f"{pid}.md", sorted((Path(folder) / "draft").glob(f"{pid}-draft-v*.md"))
    if not face.is_file() or not drafts:
        return []
    m = re.search(r"(?ms)^## Content[ \t]*\n(.*?)(?=^## |\Z)", face.read_text(encoding="utf-8", errors="replace"))
    if m and TAGGED.search(m.group(1)):
        return []
    words = len(drafts[-1].read_text(encoding="utf-8", errors="replace").split())
    return [f"its Content holds no adopted sentence, yet {drafts[-1].name} has {words} words: "
            f"page.py adopt {Path(folder).name}, then export, then build"]
