import json
import csv
import os

class MonsterList:

    def __init__(self):
        """
        Parses JSON files of 5e monsters for data maipulation.

        :param data_dir: strong of the relative path of the data directory.
        """
        self.monsters = []
        self.monster_index = dict()

    def _add_monsters(self, data):
        self.monsters.extend(data)

    def add_json_monsters(self, filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            self._add_monsters(data["monster"])

    def add_json_filelist(self, filepath_list):
        for filepath in filepath_list:
            self.add_json_monsters(filepath)

    def index_monster_byname(self):
        for monster in self.monsters:
            self.monster_index[monster["name"]] = monster

    def silvered_list(self):
        monster_names = []
        for name, monster in self.monster_index.items():
            i_note = self._get_nested_field_note('immune', monster)
            r_note = self._get_nested_field_note('resist', monster)
            if "silvered" in i_note or "silvered" in r_note:
                monster_names.append(name)
        return monster_names

    def _get_nested_field_note(self, fieldname, data):
        notes = []
        if fieldname in data and data[fieldname] is not None:
            for item in data[fieldname]:
                if isinstance(item, dict) and 'note' in item:
                    notes.append(item['note'])
        return ' '.join(notes)

    def get_hp_range(self):
        """
        "cr": "1",
        "hp": {
            "average": 10,
            "formula": "3d4 + 3"
            }

        :return:
        """
        hp_range = dict()
        for monster in self.monsters:
            if 'cr' in monster and 'hp' in monster:
                if 'average' in monster['hp']:
                    cr = self._get_cr(monster)
                    hp_range[cr] = hp_range.get(cr, {
                        'min': 10000000000,
                        'min_name': '',
                        'max': 0,
                        'max_name': ''
                    })
                    hp = self._get_hp_average(monster)
                    if hp < hp_range[cr]["min"]:
                        hp_range[cr]["min"] = hp
                        hp_range[cr]["min_name"] = monster["name"]
                    if hp > hp_range[cr]["max"]:
                        hp_range[cr]["max"] = hp
                        hp_range[cr]["max_name"] = monster["name"]
        return hp_range

    def _get_cr(self, m):
        """
        Crude fix to get CR.  Sometimes it's a key val, sometimes it's key, dict
        :param m:
        :return:
        """
        cr = m["cr"]
        if isinstance(cr, dict):
            cr = cr["cr"]
        return cr

    def _get_hp_average(self, m):
        """
        Crude fix to get HP average
        :param m:
        :return:
        """
        hp = m["hp"]["average"]
        return hp

    def write_hp_range_csv(self, filepath):
        fieldnames = ["cr", "min", "max", "min_name", "max_name"]
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            for k, row in self.get_hp_range().items():
                row['cr'] = k
                writer.writerow(row)