from fluentogram import TranslatorHub, FluentTranslator
from fluent_compiler.bundle import FluentBundle

def get_hub():
    t_hub = TranslatorHub(
        locales_map = {
            "en": ("en", "ru", ),
            "ru": ("ru",)
        }, 
        translators = [
            FluentTranslator(
                locale='en', 
                translator=FluentBundle.from_files(
                    locale='en-US', 
                    filenames=['tgbot/language/locales/en.ftl', ],
                )
            ),
            FluentTranslator(
                locale='ru', 
                translator=FluentBundle.from_files(
                    locale='ru-RU', 
                    filenames=['tgbot/language/locales/ru.ftl', ],
                )
            )
        ],
        root_locale='ru',
    )
    return t_hub


class Translator:
    t_hub: TranslatorHub

    def __init__(self):
        self.t_hub = get_hub()
    
    def __call__(self, language: str, *args, **kwargs):
        return LocalizedTranslator(
            translator=self.t_hub.get_translator_by_locale(locale=language)
        ) 


class LocalizedTranslator:
    translator: Translator

    def __init__(self, translator: Translator):
        self.translator = translator

    def get(self, key: str, **kwargs) -> str:
        return self.translator.get(key, **kwargs)
