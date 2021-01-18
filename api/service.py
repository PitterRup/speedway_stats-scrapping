import logging

import requests

from speedway_data_parser.interpreters import ParsedTeamMatchInterpreter
from speedway_data_parser.parsers import TeamMatchParserBuilder

log = logging.getLogger(__name__)


def team_match_parsing(url):
    log.info(u'Do request to url={}'.format(url))
    ret = requests.get(url)
    parser = TeamMatchParserBuilder.by_url(url)
    parser.parse(ret.text)
    parser_proxy = ParsedTeamMatchInterpreter(parser)
    return {
        'stadium': parser_proxy.get_stadium,
        'round': parser_proxy.get_round,
        'match_date': parser_proxy.get_match_datetime,
        'referee': parser_proxy.get_referee,
        'track_commisioner': parser_proxy.get_track_commissioner,
        'first_team': {
            'name': parser_proxy.get_first_team_name,
            'score': parser_proxy.get_first_team_score,
            'composition': parser_proxy.get_first_team_composition,
        },
        'second_team': {
            'name': parser_proxy.get_second_team_name,
            'score': parser_proxy.get_second_team_score,
            'composition': parser_proxy.get_second_team_composition,
        },
        'heats': parser_proxy.get_heats,
    }
