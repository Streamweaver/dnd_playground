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


def saves_count(data):
    """
    Counts the save proficiencies of monsters.

    :param data:
    :return:
    """
    d_saves = dict()
    for m in data:
        for save in [x.strip() for x in m["Sav. Throws"].split(",") if m["Sav. Throws"] != "None"]:
            d_saves[save] = d_saves.get(save, 0) + 1
    return d_saves



# RESISTANCES

class WriParser:

    def __init__(self, data):
        self.totals = self._wri_count(data)
        self.totals_by_cr = dict()
        self.dmg_type_breakdown = dict()
        self.dmg_type_bycr_breakdown = dict()
        self.wri_indexer()

    def _wri_count(self, data):
        """
        Counts the WRI by type.
        :param data:
        :return:
        """
        d_wri = dict()
        for m in data:
            for wri in [x.strip() for x in m["WRI"].split(",")]:
                d_wri[wri.lower()] = d_wri.get(wri.lower(), 0) + 1
        return d_wri

    def wri_count_by_cr(self, data):
        """
        Counts the WRI by type grouped by CR.
        :param data:
        :return:
        """
        p = re.compile(r"(.*)(immu|res|weak)")
        wri_by_cr = dict()
        for m in data:
            if m["CR"] != "VARIES":
                cr = float(m["CR"])
                for wri in [x.strip().lower() for x in m["WRI"].split(",")]:
                    if wri != 'none':
                        m = p.match(wri)
                        dmg_type, wri_type = m.groups()
                        if dmg_type not in wri_by_cr:
                            wri_by_cr[dmg_type] = [0] * 15
                        offset = self._wri_row_offset(cr, wri_type)
                        wri_by_cr[dmg_type][offset] = wri_by_cr[dmg_type][offset] + 1
        return wri_by_cr


    def _wri_row_offset(self, cr, wri):
        """
        Returns an int of the row offset for the wri by cr
        :param cr: float of cr
        :param wri: one of weak, res, immu
        :return: int
        """
        offset = 0
        if cr <= 5.0:
            offset += 0
        if 6.0 <= cr <= 10.0:
            offset += 3
        if 11.0 <= cr <= 15.0:
            offset += 6
        if 16.0 <= cr <= 20.0:
            offset += 9
        if cr >= 21.0:
            offset += 12

        if wri == 'weak':
            offset += 0
        if wri == 'res':
            offset += 1
        if wri == 'immu':
            offset += 2

        return offset

    def wri_indexer(self):
        """
        Takes a list of dicts with resistance name keys and count items.

        :param data:
        :return:
        """
        p = re.compile(r"(.*)(immu|res|weak)")
        for item in self.totals.keys():
            if item != 'none':
                m = p.match(item)
                self._init_dmg_type(m.group(1))
                # example: 0: 'acidimmu, 1: 'acid', 2: 'immu'
                # 0 raw_key, 1 dmg_type, 2 wri
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

