import csv
from dnd_data.monstersheetparser import monster_language_count, WriParser
from dnd_data.spellsheetparser import SpellData
from dnd_data.util import parse_csv


def write_language_csv(data):
    languages = monster_language_count(data)
    with open('monster_language_count.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in sorted(languages.items()):
            writer.writerow(item)


def write_wri_csv(data):
    fieldnames = ['label', 'weak', 'res', 'immu']
    with open('damage_wri_counts.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for k, item in data.items():
            writer.writerow(item)


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
    data = parse_csv('data/phb_spells.csv')
    spells = SpellData(data)
    write_spell_save_types(spells.save_type_totals)

