from . import eng_lexicon, ru_lexicon, es_lexicon

LANGUAGE_CODES = ('ru', 'en', 'es')


async def get_lexicon(language_code: str | None):
    if language_code is None or language_code not in LANGUAGE_CODES or language_code == 'en':
        return eng_lexicon
    elif language_code == 'es':
        return es_lexicon
    return ru_lexicon
