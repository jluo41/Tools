"""Every page section's emoji, one table (hai-ui A12). The title's section menu, the section heading and a theme's
shared sections all read it, so a plain Block and a theme Block name the same section the same way.

    section_label("studio", "Studio")  -> "🎨 Studio"
"""

SECTION_ICONS = {
    "report": "📋", "jobs": "💼", "work": "🧪", "studio": "🎨", "interactions": "🙋", "decisions": "⚖️",
    "know": "📚", "checklist": "📝", "timeline": "🕒", "skills": "🧰", "files": "📁", "delivery": "📦",
    "related": "🔗",
}


def section_label(key: str, name: str) -> str:
    """The section's name with its emoji in front; a name that already starts with it is returned as it is."""
    icon = SECTION_ICONS.get(key, "")
    if not icon or name.startswith(icon):
        return name
    return f"{icon} {name}"
