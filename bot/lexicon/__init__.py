from . import eng_lexicon, ru_lexicon


def get_lexicon(language_code: str | None):
    if language_code is None or language_code != 'ru':
        return eng_lexicon
    return ru_lexicon
