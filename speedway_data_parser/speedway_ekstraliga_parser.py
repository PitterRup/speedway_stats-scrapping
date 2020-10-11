from lxml import html
from datetime import datetime
import re

from speedway_data_parser.util import catch_exceptions
from speedway_data_parser.string_tools import strip
from speedway_data_parser.types import (
    TeamCompositionRider,
    Heat,
    HeatRider,
)


class Parser():
    def __init__(self, html_string):
        self.tree = html.fromstring(html_string)

    @catch_exceptions(IndexError)
    def get_stadium(self):
        elem = self.tree.find_class('match__header__info')[0].getchildren()[0]
        return elem.text.strip()

    @catch_exceptions(IndexError)
    def get_round(self):
        elem = self.tree.find_class('match__header__info')[0].getchildren()[1]
        return elem.text.strip()

    @catch_exceptions(IndexError)
    def get_match_datetime(self):
        str_date = self.tree.find_class('match__header__datetime')[0].text.strip()
        return datetime.strptime(str_date, '%d.%m.%Y, %H:%M')

    @catch_exceptions(IndexError)
    def get_referee(self):
        elem = self.tree.find_class('match__header__members')[0].getchildren()[0]
        return elem.text_content().strip().replace('Sędzia\n', '')

    @catch_exceptions(IndexError)
    def get_track_commissioner(self):
        elem = self.tree.find_class('match__header__members')[0].getchildren()[1]
        return elem.text_content().strip().replace('Komisarz toru\n', '')

    @catch_exceptions(IndexError)
    def get_first_team_name(self):
        return self.tree.find_class('match__header__points__col__header')[0].text.strip()

    @catch_exceptions((IndexError, ValueError))
    def get_first_team_score(self):
        return int(self.tree.find_class('match__header__points__col__header__score')[0].text.strip())

    @catch_exceptions(IndexError)
    def get_second_team_name(self):
        return self.tree.find_class('match__header__points__col__header')[1].text.strip()

    @catch_exceptions((IndexError, ValueError))
    def get_second_team_score(self):
        return int(self.tree.find_class('match__header__points__col__header__score')[1].text.strip())

    @catch_exceptions(IndexError)
    def get_first_team_composition(self):
        table = self.tree.find_class('match__header__points__col')[0].xpath('table')[0]
        return self.get_team_composition(table)

    @catch_exceptions(IndexError)
    def get_second_team_composition(self):
        table = self.tree.find_class('match__header__points__col')[1].xpath('table')[0]
        return self.get_team_composition(table)

    def get_team_composition(self, elem_table):
        ret = []
        for row in elem_table.xpath('tr'):
            ret.append(TeamCompositionRider(
                number=int(row.find_class('match__header__points__no')[0].text.strip()),
                name=row.find_class('match__header__points__rider')[0].text_content().strip(),
            ))
        return ret

    def get_heats(self):
        heat_parser = HeatParser()
        ret = []
        for elem_heat in self.tree.find_class('match__heat'):
            header = elem_heat.getchildren()[0].text.strip()
            riders = heat_parser.get_heat_riders(elem_heat.xpath('table')[0].xpath('tr'))
            ret.append(Heat(
                number=int(heat_parser.get_heat_number(header)),
                winner_time=heat_parser.get_heat_winner_timer(header),
                rider_a=riders[0],
                rider_b=riders[1],
                rider_c=riders[2],
                rider_d=riders[3],
            ))
        return ret


class HeatParser():
    def get_heat_number(self, header):
        return re.search('(?<=Bieg )[0-9]{1,2}', header).group()

    def get_heat_winner_timer(self, header):
        g = re.search('[0-9]{2}.[0-9]{2}', header)
        if not g:
            return None
        return float(g.group())

    def get_heat_riders(self, lst_elem_rider):
        ret = []
        for rider in lst_elem_rider:
            lst_name = rider.getchildren()[2].getchildren()
            if len(lst_name) > 1:
                name = lst_name[1].text.strip()
                replaced_name = lst_name[0].text.strip()
            else:
                name = lst_name[0].text.strip()
                replaced_name = None
            ret.append(HeatRider(
                warning=strip(rider.getchildren()[1].text_content()) == '!',
                name=name,
                replaced_rider_name=replaced_name,
                score=strip(rider.getchildren()[3].text),
            ))
        return ret
