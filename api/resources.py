import logging

from flask import g
from flask_restful import Resource

from api.ma_schemas import (ParaSeasonMatchesParsing, ParaTeamMatchParsing,
                            ParaTeamParsing)
from api.service import (season_matches_parsing, team_match_parsing,
                         team_parsing)
from api.util.marshmallow_tools import validate_ma

log = logging.getLogger(__name__)


class ParseTeamMatch(Resource):

    @validate_ma(ParaTeamMatchParsing)
    def post(self):
        para = g.req_para
        log.info('Receive request to parser match from para={}'.format(para))
        try:
            return team_match_parsing(para['url'])
        except ConnectionError as e:
            return {'message': 'Errors occured during process', u'error': str(e)}, 500


class ParseTeam(Resource):

    @validate_ma(ParaTeamParsing)
    def post(self):
        para = g.req_para
        log.info('Receive request to parse team from para={}'.format(para))
        try:
            return team_parsing(para['url'])
        except ConnectionError as e:
            return {'message': 'Errors occured during process', u'error': str(e)}, 500


class ParseSeasonMatches(Resource):
    @validate_ma(ParaSeasonMatchesParsing)
    def post(self):
        para = g.req_para
        log.info('Receive request to parse season matches from para={}'.format(para))
        try:
            return season_matches_parsing(para['season'])
        except ConnectionError as e:
            return {'message': 'Errors occured during process', u'error': str(e)}, 500
