import enum
import json
import logging
import os

LOGGER = logging.getLogger("i18n")


class I18nManager:
    def __init__(self, locale_directory='locales', default_locale='en'):
        self.locale_directory = locale_directory
        self.translations = {}
        self.default_locale = default_locale
        self.load_translations()

    def load_translations(self):
        for filename in os.listdir(self.locale_directory):
            if filename.endswith('.json'):
                locale = filename.split('.')[0]
                with open(os.path.join(self.locale_directory, filename), 'r', encoding='utf-8') as file:
                    self.translations[locale] = json.load(file)

    def get(self, key, locale=None) -> str:
        return self.translations.get(locale or self.default_locale, {}).get(key, key)


class Keys(enum.Enum):
    RAN_OUT_QUESTIONS = 'ran_out_questions'
    COUNTDOWN = 'countdown'
