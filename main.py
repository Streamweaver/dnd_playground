import csv
import pprint
from dnd_data.monstersheetparser import monster_language_count, WriParser, saves_count
from dnd_data.spellsheetparser import SpellData
from dnd_data.monster_data import MonsterList
from dnd_data.spell_data import SpellList
from dnd_data.util import parse_csv

def write_monster_save_csv(data):
    m_saves = saves_count(data)
    with open('monster_saves_count.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in sorted(m_saves.items()):
            writer.writerow(item)

def write_language_csv(data):
    languages = monster_language_count(data)
    with open('monster_language_count.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in sorted(languages.items()):
            writer.writerow(item)


def write_wri_csv(data):
    fieldnames = ['label', 'weak', 'res', 'immu']
    with open('monster_wri_counts.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for k, item in data.items():
            writer.writerow(item)

def write_wri_bycr_csv(data):
    with open('monster_wri_bycr.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for dmg_type, wri_list in data.items():
            writer.writerow([dmg_type] + data[dmg_type])


def write_spell_damage_types(data):
    with open('spell_damage_types.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in sorted(data.items()):
            writer.writerow(item)


def write_spell_save_types(data):
    with open('spell_save_types.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in sorted(data.items()):
            writer.writerow(item)

def write_spell_data():
    spell_list = SpellList()
    spell_list.parse_json_files([
        'data/spells/spells-phb.json',
        'data/spells/spells-xge.json',
        'data/spells/spells-tce.json'
    ])
    condition_data = spell_list.calculate_condition_types()
    damage_data = spell_list.calculate_damage_types()

    spell_list.write_inflict_type_csv('spell_damage_types_bylevel.csv', damage_data, spell_list.level_fieldnames)
    spell_list.write_inflict_type_csv('spell_condition_types_bylevel.csv', condition_data, spell_list.level_fieldnames)

    spell_list.write_inflict_type_csv('spell_damage_types_byclass.csv', damage_data, spell_list.class_fieldnames)
    spell_list.write_inflict_type_csv('spell_condition_types_byclass.csv', condition_data, spell_list.class_fieldnames)


    spell_list.write_inflict_type_csv("spell_save_byclass.csv",
                                      spell_list.calculate_savingthrow_type(),
                                      spell_list.class_fieldnames)


def monster_list():
    m_list = MonsterList()
    filelist = ["data/bestiary/%s" % x for x in [
        'bestiary-ai.json',
        'bestiary-bgdia.json',
        'bestiary-cm.json',
        'bestiary-cos.json',
        'bestiary-dc.json',
        'bestiary-dip.json',
        'bestiary-dmg.json',
        'bestiary-egw.json',
        'bestiary-erlw.json',
        'bestiary-esk.json',
        'bestiary-ggr.json',
        'bestiary-gos.json',
        'bestiary-hftt.json',
        'bestiary-hotdq.json',
        'bestiary-idrotf.json',
        'bestiary-imr.json',
        'bestiary-kkw.json',
        'bestiary-llk.json',
        'bestiary-lmop.json',
        'bestiary-lr.json',
        'bestiary-mag.json',
        'bestiary-mff.json',
        'bestiary-mm.json',
        'bestiary-mot.json',
        'bestiary-mtf.json',
        'bestiary-oota.json',
        'bestiary-oow.json',
        'bestiary-phb.json',
        'bestiary-pota.json',
        'bestiary-ps-a.json',
        'bestiary-ps-d.json',
        'bestiary-ps-i.json',
        'bestiary-ps-k.json',
        'bestiary-ps-x.json',
        'bestiary-ps-z.json',
        'bestiary-rmbre.json',
        'bestiary-rot.json',
        'bestiary-sads.json',
        'bestiary-sdw.json',
        'bestiary-vgm.json',
        'bestiary-wdh.json',
        'bestiary-wdmm.json',
        'bestiary-xge.json'
    ]]
    m_list.add_json_filelist(filelist)
    m_list.write_hp_range_csv('monster_hp_range.csv')


if __name__ == "__main__":
    spell_list = SpellList()
    spell_list.parse_json_files([
        'data/spells/spells-phb.json',
        'data/spells/spells-xge.json',
        'data/spells/spells-tce.json'
    ])
    print(len(spell_list.spells))

