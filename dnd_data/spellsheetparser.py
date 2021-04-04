
class SpellData:

    def __init__(self, data):
        self.data = data
        self.damage_type_totals = dict()
        self.save_type_totals = dict()
        self._count_damage_types()
        self._parse_saves()


    def _count_damage_types(self):
        for dt in [x["Damage Type"].strip().lower() for x in self.data]:
            if dt:
                self.damage_type_totals[dt] = self.damage_type_totals.get(dt, 0) + 1

    def _parse_saves(self):
        save_list = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        for save in [x["Attack/Saving Throw (Effect)"].strip() for x in self.data]:
            if save and save[:3] in save_list:
                self.save_type_totals[save[:3]] = self.save_type_totals.get(save[:3], 0) + 1

