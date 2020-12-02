
class ParsedTeamMatchInterpreter:
    def __init__(self, parsed_data):
        u'''
        :param `TeamMatchParser` parsed_data: obiekt sparsowanych danych
        u'''
        self.parsed_data = parsed_data

    def __getattr__(self, item):
        if item == 'get_heats':
            heats = self.parsed_data.get_heats()
            self.dct_first_team_composition = {
                rider.name: rider.number
                for rider in self.parsed_data.get_first_team_composition()
            }
            self.dct_second_team_composition = {
                rider.name: rider.number
                for rider in self.parsed_data.get_second_team_composition()
            }
            ret = []
            for heat in heats:
                dct_heat = heat._asdict()
                dct_rider_a = dct_heat['rider_a']._asdict()
                dct_rider_b = dct_heat['rider_b']._asdict()
                dct_rider_c = dct_heat['rider_c']._asdict()
                dct_rider_d = dct_heat['rider_d']._asdict()
                dct_rider_a['number'], dct_rider_a['team'] = self.identify_rider(dct_rider_a['name'])
                dct_rider_b['number'], dct_rider_b['team'] = self.identify_rider(dct_rider_b['name'])
                dct_rider_c['number'], dct_rider_c['team'] = self.identify_rider(dct_rider_c['name'])
                dct_rider_d['number'], dct_rider_d['team'] = self.identify_rider(dct_rider_d['name'])
                dct_heat['rider_a'] = dct_rider_a
                dct_heat['rider_b'] = dct_rider_b
                dct_heat['rider_c'] = dct_rider_c
                dct_heat['rider_d'] = dct_rider_d
                ret.append(dct_heat)
            return ret
        else:
            return getattr(self.parsed_data, item)

    def identify_rider(self, rider_name):
        number = self.dct_first_team_composition.get(rider_name)
        if number:
            return number, 'first'
        number = self.dct_second_team_composition.get(rider_name)
        if number:
            return number, 'second'
        raise ValueError("Rider {} wasn't identified".format(rider_name))
