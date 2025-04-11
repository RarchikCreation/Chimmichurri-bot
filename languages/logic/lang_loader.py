import json
import os

from data.config import GLOBAL_LANG_FILE

def load_global_language():
    if os.path.exists(GLOBAL_LANG_FILE):
        with open(GLOBAL_LANG_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("language", "ru")
    return "ru"

def save_global_language(lang):
    with open(GLOBAL_LANG_FILE, "w", encoding="utf-8") as f:
        json.dump({"language": lang}, f, ensure_ascii=False, indent=4)


def load_language(lang: str):
    try:
        with open(f"languages/files/lang_{lang.upper()}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_current_language():
    if os.path.exists(GLOBAL_LANG_FILE):
        with open(GLOBAL_LANG_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("language", "ru")
    return "ru"

languages = {
    "ru": load_language("ru"),
    "eng": load_language("eng")
}
