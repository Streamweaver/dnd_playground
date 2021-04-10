import json
import csv


class SpellList:

    def __init__(self):
        self.spells = []
        self.level_fieldnames = ['type', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "total"]
        class_list = sorted(['Bard', 'Druid', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard',
                                 'Cleric', 'Paladin', 'Artificer', 'Monk'])
        class_list.insert(0, 'type')
        class_list.append('total')
        self.class_fieldnames = class_list

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

    def write_inflict_type_csv(self, filepath, data, fieldnames):
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            for k, raw_row in data.items():
                row = {key: value for key, value in raw_row.items() if key in fieldnames}
                row['type'] = k.title()
                writer.writerow(row)

    def calculate_inflict(self, inflict_type):
        inflict_totals = dict()
        for spell in self.spells:
            for inflict in spell.get(inflict_type, []):
                if inflict not in inflict_totals:
                    inflict_totals[inflict] = dict()
                self._increment_level(inflict_totals[inflict], spell["level"])
                self._increment_class(inflict_totals[inflict], spell["classes"])
                inflict_totals[inflict]["total"] = \
                    inflict_totals[inflict].get("total", 0) + 1
        return inflict_totals

    def _increment_level(self, d, lvl):
        d[lvl] = d.get(lvl, 0) + 1

    def _increment_class(selfd, d, classes):
        for character_class in classes.get('fromClassList', []):
            d[character_class["name"]] = d.get(character_class["name"], 0) + 1