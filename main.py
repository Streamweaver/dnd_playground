import csv
import pprint
from dnd_data.monstersheetparser import monster_language_count, WriParser, saves_count
from dnd_data.spellsheetparser import SpellData
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


if __name__ == "__main__":
    spell_list = SpellList()
    spell_list.parse_json_files([
        'data/spells/spells-phb.json',
        'data/spells/spells-xge.json',
        'data/spells/spells-tce.json'
    ])
    print(spell_list.calculae_range_type())

