"""Keep track of what was already covered last week, to avoid repeating it."""
import json
import os

HISTORY_FILE = "history/previous_newsletter.json"


def load_previous_items():
    """Return a flat list of previously covered item texts.
    Returns an empty list the first time (no history file yet)."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    items = []
    for section in data.get("sections", []):
        for item in section.get("items", []):
            text = item.get("text", "")
            if text:
                items.append(text)
    return items


def save_current_content(content):
    """Persist this week's content so next week's run can avoid repeating it."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
