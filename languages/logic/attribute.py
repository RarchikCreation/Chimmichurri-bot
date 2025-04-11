from languages.logic.lang_loader import languages, get_current_language

def get_lang_data():
    current_lang = get_current_language()
    return languages.get(current_lang, {})
