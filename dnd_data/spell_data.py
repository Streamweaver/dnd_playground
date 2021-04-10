import json
import csv


class SpellList:

    def __init__(self):
        self.spells = []

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
        return self.calculate_inflict('damageInflict')

    def calculate_condition_types(self):
        return self.calculate_inflict('conditionInflict')

    def write_inflict_type_csv(self, filepath, data):
        fieldnames = ['type', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "total"]
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            for k, row in data.items():
                row['type'] = k.title()
                writer.writerow(row)

    def calculate_inflict(self, inflict_type):
        inflict_totals = dict()
        for spell in self.spells:
            for inflict in spell.get(inflict_type, []):
                if inflict not in inflict_totals:
                    inflict_totals[inflict] = dict()
                inflict_totals[inflict][spell["level"]] = \
                    inflict_totals[inflict].get(spell["level"], 0) + 1
                inflict_totals[inflict]["total"] = \
                    inflict_totals[inflict].get("total", 0) + 1
        return inflict_totals

