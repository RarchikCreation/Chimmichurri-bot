from languages.logic.lang_loader import languages, get_current_language

current_lang = get_current_language()
lang_data = languages.get(current_lang, {})