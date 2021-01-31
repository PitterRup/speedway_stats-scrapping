from datetime import datetime

import pytest

from speedway_data_parser.global_consts import DctHelmetColor
from speedway_data_parser.parsers.speedway_ekstraliga_parser import \
    TeamMatchParser
from speedway_data_parser.types import Heat, HeatRider, TeamCompositionRider


@pytest.fixture(scope="module")
def test_html_match():
    with open("tests/dane_testowe/speedway_ekstraliga_match.html", "r") as f:
        html = f.read()
    tmp = TeamMatchParser()
    tmp.parse(html)
    return tmp


class TestMatchParser:
    def test_get_stadium(self, test_html_match):
        assert test_html_match.get_stadium() == "Stadion im. Edwarda Jancarza"

    def test_get_round(self, test_html_match):
        assert test_html_match.get_round() == 16

    def test_get_match_datetime(self, test_html_match):
        assert test_html_match.get_match_datetime() == datetime(2020, 10, 4, 19, 15)

    def test_get_referee(self, test_html_match):
        assert test_html_match.get_referee() == "Piotr Lis"

    def test_get_track_commissioner(self, test_html_match):
        assert test_html_match.get_track_commissioner() == "Arkadiusz Kalwasiński"

    def test_get_first_team_name(self, test_html_match):
        assert test_html_match.get_first_team_name() == "MOJE BERMUDY STAL Gorzów"

    def test_get_first_team_score(self, test_html_match):
        assert test_html_match.get_first_team_score() == 55

    def test_get_second_team_name(self, test_html_match):
        assert test_html_match.get_second_team_name() == "BETARD SPARTA Wrocław"

    def test_get_second_team_score(self, test_html_match):
        assert test_html_match.get_second_team_score() == 34

    def test_get_first_team_composition(self, test_html_match):
        ret = test_html_match.get_first_team_composition()
        assert isinstance(ret, list)
        assert len(ret) == 8
        for obj in ret:
            assert isinstance(ret[0], TeamCompositionRider)

    def test_get_second_team_composition(self, test_html_match):
        ret = test_html_match.get_second_team_composition()
        assert isinstance(ret, list)
        assert len(ret) == 8
        for obj in ret:
            assert isinstance(ret[0], TeamCompositionRider)

    def test_get_heats(self, test_html_match):
        heats = test_html_match.get_heats()
        assert isinstance(heats, list)
        assert len(heats) == 17
        for heat in heats:
            assert isinstance(heat, Heat)
            assert isinstance(heat.rider_a, HeatRider)
            assert isinstance(heat.rider_b, HeatRider)
            assert isinstance(heat.rider_c, HeatRider)
            assert isinstance(heat.rider_d, HeatRider)

    @pytest.mark.parametrize(
        "header, exp_number", [("Bieg 1", 1), ("Powtórka Bieg 1", 1), ("Powtórka Bieg 1 - 58.62s", 1)]
    )
    def test__get_heat_number(self, test_html_match, header, exp_number):
        ret = test_html_match._get_heat_number(header)
        assert isinstance(ret, int)
        assert ret == exp_number

    @pytest.mark.parametrize(
        "str_classes, exp_helmet",
        [
            ("match__heat__helmet match__heat__helmet--yellow", DctHelmetColor.YELLOW),
            ("match__heat__helmet match__heat__helmet--red", DctHelmetColor.RED),
            ("match__heat__helmet match__heat__helmet--blue", DctHelmetColor.BLUE),
            ("match__heat__helmet match__heat__helmet--white", DctHelmetColor.WHITE),
        ],
    )
    def test__get_helmet_color(self, test_html_match, str_classes, exp_helmet):
        assert test_html_match._get_helmet_color(str_classes) == exp_helmet

    @pytest.mark.parametrize(
        "header, exp_winner_time", [("Bieg 1", None), ("Powtórka Bieg 1", None), ("Powtórka Bieg 1 - 58.62s", 58.62)]
    )
    def test__get_heat_winner_time(self, test_html_match, header, exp_winner_time):
        assert test_html_match._get_heat_winner_timer(header) == exp_winner_time
