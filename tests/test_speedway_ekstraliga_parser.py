from datetime import datetime

import pytest

from speedway_data_parser.speedway_ekstraliga_parser import MatchParser


@pytest.fixture(scope="module")
def test_html_match():
    with open("tests/dane_testowe/speedway_ekstraliga_match.html", "r") as f:
        html = f.read()
    return MatchParser(html)


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
