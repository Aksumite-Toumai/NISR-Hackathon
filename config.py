from googletrans import Translator  # type: ignore


CONFIG = {
    # 'scrollZoom': False,
    # 'editable': False,
    # 'showLink': False,
    'displaylogo': False,
}

# Default language
LANG = 'en'


def translate_text(text_to_translate: str) -> str:
    try:
        if text_to_translate and LANG != "rw":
            translator = Translator()
            translated = translator.translate(text_to_translate, dest=LANG)
            return translated.text
        return text_to_translate
    except KeyError:
        return text_to_translate
