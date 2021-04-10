import json
import csv


class SpellList:

    def __init__(self):
        self.spells = []
        self.damage_totals = dict()

    def _add_spells(self, data):
        """
        Adds a list of spells.
        :param data:
        :return:
        """
        self.spells.extend(data)

    def add_json_spells(self, filepath):
        """
        Opens a json file of spells and adds the list of spells to the class.

        :param filepath:
        :return:
        """
        with open(filepath) as json_file:
            data = json.load(json_file)
            self._add_spells(data["spell"])

    def parse_json_files(self, filepath_list):
        for filepath in filepath_list:
            self.add_json_spells(filepath)

    def calculate_damage_types(self):
        self.damage_totals = dict()
        for spell in self.spells:
            for damage_type in spell.get('damageInflict', []):
                if damage_type not in self.damage_totals:
                    self.damage_totals[damage_type] = dict()
                self.damage_totals[damage_type][spell["level"]] = \
                    self.damage_totals[damage_type].get(spell["level"], 0) + 1
                self.damage_totals[damage_type]["total"] = \
                    self.damage_totals[damage_type].get("total", 0) + 1

    def write_damage_type_csv(self, filepath):
        fieldnames = ['type', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "total"]
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            for k, row in self.damage_totals.items():
                row['type'] = k
                writer.writerow(row)


