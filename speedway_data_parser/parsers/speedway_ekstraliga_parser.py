import re
from datetime import datetime

from lxml import html

from speedway_data_parser.global_consts import DctHelmetColor
from speedway_data_parser.string_tools import int_or_none, strip, upper
from speedway_data_parser.types import (Heat, HeatRider, TeamCompositionRider,
                                        TeamRider)


class TeamMatchParser:
    def parse(self, html_string):
        self.tree = html.fromstring(html_string)

    def get_stadium(self):
        elem = self.tree.find_class("match__header__info")[0].getchildren()[0]
        return elem.text.strip()

    def get_round(self):
        elem = self.tree.find_class("match__header__info")[0].getchildren()[1]
        return int(elem.text.strip().replace(" Runda", ""))

    def get_match_datetime(self):
        str_date = self.tree.find_class("match__header__datetime")[0].text.strip()
        return datetime.strptime(str_date, "%d.%m.%Y, %H:%M")

    def get_referee(self):
        elem = self.tree.find_class("match__header__members")[0].getchildren()[0]
        return elem.text_content().strip().replace("Sędzia\n", "")

    def get_track_commissioner(self):
        elem = self.tree.find_class("match__header__members")[0].getchildren()[1]
        return elem.text_content().strip().replace("Komisarz toru\n", "")

    def get_first_team_name(self):
        return self.tree.find_class("match__header__points__col__header")[0].text.strip()

    def get_first_team_score(self):
        return int(self.tree.find_class("match__header__points__col__header__score")[0].text.strip())

    def get_second_team_name(self):
        return self.tree.find_class("match__header__points__col__header")[1].text.strip()

    def get_second_team_score(self):
        return int(self.tree.find_class("match__header__points__col__header__score")[1].text.strip())

    def get_first_team_composition(self):
        table = self.tree.find_class("match__header__points__col")[0].xpath("table")[0]
        return self._get_team_composition(table)

    def get_second_team_composition(self):
        table = self.tree.find_class("match__header__points__col")[1].xpath("table")[0]
        return self._get_team_composition(table)

    def _get_team_composition(self, elem_table):
        ret = []
        for row in elem_table.xpath("tr"):
            name = row.find_class("match__header__points__rider")[0].text_content().strip()
            if not name:
                continue
            ret.append(
                TeamCompositionRider(
                    number=int(row.find_class("match__header__points__no")[0].text.strip()),
                    name=name,
                )
            )
        return ret

    def get_heats(self):
        ret = []
        for elem_heat in self.tree.find_class("match__heat"):
            header = elem_heat.getchildren()[0].text.strip()
            riders = self._get_heat_riders(elem_heat.xpath("table")[0].xpath("tr"))
            ret.append(
                Heat(
                    number=self._get_heat_number(header),
                    winner_time=self._get_heat_winner_timer(header),
                    rider_a=riders[0],
                    rider_b=riders[1],
                    rider_c=riders[2],
                    rider_d=riders[3],
                )
            )
        return ret

    def _get_heat_number(self, header):
        g = re.search("(?<=Bieg )[0-9]{1,2}", header)
        if not g:
            raise Exception('Nie znaleziono numeru biegu w header: "%s"' % header)
        return int(g.group())

    def _get_heat_winner_timer(self, header):
        g = re.search("[0-9]{2}.[0-9]{2}", header)
        if not g:
            return None
        return float(g.group())

    def _get_heat_riders(self, lst_elem_rider):
        ret = []
        for rider in lst_elem_rider:
            lst_name = rider.getchildren()[2].getchildren()
            if len(lst_name) > 1:
                name = lst_name[1].text.strip()
                replaced_name = lst_name[0].text.strip()
            else:
                name = lst_name[0].text.strip()
                replaced_name = None
            score_str = upper(strip(rider.getchildren()[3].text))
            if score_str not in ("D", "U", "W", "M", "T", "-", "0", "1", "2", "3", None):
                raise Exception("Nieznana wartość w polu wynik: {}".format(score_str))
            ret.append(
                HeatRider(
                    warning=strip(rider.getchildren()[1].text_content()) == "!",
                    name=name,
                    replaced_rider_name=replaced_name,
                    score=int_or_none(score_str),
                    defect=score_str == "D",
                    fall=score_str == "U",
                    exclusion=score_str in ("W", "M", "-"),
                    helmet_color=self._get_helmet_color(rider.getchildren()[0].get("class")),
                )
            )
        return ret

    def _get_helmet_color(self, str_classes):
        if "yellow" in str_classes:
            return DctHelmetColor.YELLOW
        elif "red" in str_classes:
            return DctHelmetColor.RED
        elif "blue" in str_classes:
            return DctHelmetColor.BLUE
        elif "white" in str_classes:
            return DctHelmetColor.WHITE
        else:
            raise Exception("Nie znaleziono koloru kasku w: {}".format(str_classes))


class TeamParser():
    def __init__(self, year):
        self.year = year

    def parse(self, html_string):
        self.tree = html.fromstring(html_string)

    def get_year(self):
        return self.year

    def get_team_name(self):
        return self.tree.find_class('page-team__top__left__title')[0].text.strip()

    def get_team_members(self):
        riders = []
        for rider in self.tree.find_class('page-team__riders')[0].getchildren():
            riders.append(TeamRider(
                firstname=rider.find_class('page-team__rider__name')[0].text.strip(),
                surname=rider.find_class('page-team__rider__surname')[0].text.strip(),
                birthdate=datetime.strptime(
                    rider.find_class('page-team__rider__birthdate')[0].text.strip(),
                    "%d.%m.%Y"
                ),
                country=rider.find_class('page-team__rider__country')[0].text.strip(),
            ))
        return riders
