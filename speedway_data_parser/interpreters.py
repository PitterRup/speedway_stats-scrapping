from speedway_data_parser.types import InterpretedHeat, InterpretedHeatRider


class ParsedTeamMatchInterpreter:
    def __init__(self, parsed_data):
        u'''
        :param `TeamMatchParser` parsed_data: obiekt sparsowanych danych
        u'''
        self.parsed_data = parsed_data
        self.dct_first_team_composition = {
            rider.name: rider.number
            for rider in self.parsed_data.get_first_team_composition()
        }
        self.dct_second_team_composition = {
            rider.name: rider.number
            for rider in self.parsed_data.get_second_team_composition()
        }

    def __getattr__(self, item):
        if item == 'get_heats':
            heats = self.parsed_data.get_heats()
            ret = []
            for heat in heats:
                dct_heat = heat._asdict()
                (
                    dct_heat['rider_a'],
                    dct_heat['rider_b'],
                    dct_heat['rider_c'],
                    dct_heat['rider_d'],
                ) = self.identify_riders(heat)
                ret.append(InterpretedHeat._make(dct_heat.values()))
            return ret
        else:
            return getattr(self.parsed_data, item)()

    def identify_riders(self, heat):
        dct_rider_a = heat.rider_a._asdict()
        dct_rider_b = heat.rider_b._asdict()
        dct_rider_c = heat.rider_c._asdict()
        dct_rider_d = heat.rider_d._asdict()
        dct_rider_a['number'], dct_rider_a['team'] = self.identify_rider(dct_rider_a['name'])
        dct_rider_b['number'], dct_rider_b['team'] = self.identify_rider(dct_rider_b['name'])
        dct_rider_c['number'], dct_rider_c['team'] = self.identify_rider(dct_rider_c['name'])
        dct_rider_d['number'], dct_rider_d['team'] = self.identify_rider(dct_rider_d['name'])
        return (
            InterpretedHeatRider._make(dct_rider_a.values()),
            InterpretedHeatRider._make(dct_rider_b.values()),
            InterpretedHeatRider._make(dct_rider_c.values()),
            InterpretedHeatRider._make(dct_rider_d.values()),
        )

    def identify_rider(self, rider_name):
        number = self.dct_first_team_composition.get(rider_name)
        if number:
            return number, 'first'
        number = self.dct_second_team_composition.get(rider_name)
        if number:
            return number, 'second'
        raise ValueError("Rider {} wasn't identified".format(rider_name))
