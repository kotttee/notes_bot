from fluentogram import TranslatorHub
from .languages.build import build_translations


async def build_translator_hub(required_languages: list) -> TranslatorHub:
    auxiliary_dict = {}
    auxiliary_list = required_languages.copy()

    for lang in required_languages:
        auxiliary_dict[lang] = tuple(auxiliary_list)
        auxiliary_list.remove(lang)

    return TranslatorHub(
        {code: auxiliary_dict[code] for code in required_languages},
        await build_translations(required_languages)
    )
