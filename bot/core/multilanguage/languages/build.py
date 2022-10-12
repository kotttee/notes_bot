from fluentogram import FluentTranslator
from fluent_compiler.bundle import FluentBundle
from .data import *


async def build_translations(codes: list) -> list:
    translations = []
    for lang_code in codes:
        translations.append(FluentTranslator(lang_code, translator=FluentBundle.from_files(lang_code,
                                             filenames=[f"bot/core/multilanguage/languages/data/{lang_code}.ftl"])))

    return translations
