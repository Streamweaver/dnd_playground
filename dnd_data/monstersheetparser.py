import re


# LANGUAGES
def monster_language_set(data):
    """
    Returns a set of the unique elements of a monster dict field.
    :param data:
    :return: Set of unique values.
    """
    languages = set()
    for m in data:
        languages.update([x.strip() for x in m["Languages"].split(",")])
    return languages


def monster_language_count(data):
    """
    Returns a dict listing the language spoken and the number of monsters that speak it.
    :param data:
    :return:
    """
    d_lang = dict()
    for m in data:
        for lang in [x.strip() for x in m["Languages"].split(",")]:
            lang = _lang_filter(lang)
            d_lang[lang] = d_lang.get(lang, 0) + 1
    return d_lang


def _lang_filter(text):
    lang_fixed = text.lower()
    if lang_fixed.startswith('telepathy'):
        lang_fixed = 'telepathy'
    return lang_fixed


# SENSES
def senses_count(data):
    """
    Returns a dict listing the sense as the key and number of monsters with it.
    :param data:
    :return:
    """
    d_senses = dict()
    for m in data:
        for sense in [x.strip() for x in m["Senses"].split(",")]:
            d_senses[sense.lower()] = d_senses.get(sense.lower(), 0) + 1
    return d_senses


# RESISTANCES

class WriParser:

    def __init__(self, data):
        self.totals = self._wri_count(data)
        self.dmg_type_breakdown = dict()
        self.wri_indexer()

    def _wri_count(self, data):
        d_wri = dict()
        for m in data:
            for wri in [x.strip() for x in m["WRI"].split(",")]:
                d_wri[wri.lower()] = d_wri.get(wri.lower(), 0) + 1
        return d_wri

    def wri_indexer(self):
        """
        Takes a list of dicts with resistance name keys and count items.

        :param data:
        :return:
        """
        p = re.compile(r"(.*)(immu|res|weak)")
        labels = []
        for item in self.totals.keys():
            if item != 'none':
                m = p.match(item)
                self._init_dmg_type(m.group(1))
                # print(m.group(0), m.group(1), m.group(2))
                self._add_wri_count(m.group(0), m.group(1), m.group(2))

    def _init_dmg_type(self, dmg_type):
        if dmg_type not in self.dmg_type_breakdown:
            self.dmg_type_breakdown[dmg_type] = {
                'label': dmg_type,
                'weak': 0,
                'res': 0,
                'immu': 0
            }

    def _add_wri_count(self, raw_key, dmg_type, wri):
        self.dmg_type_breakdown[dmg_type][wri] = self.totals[raw_key]

