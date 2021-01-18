import logging

from flask import g
from flask_restful import Resource

from api.ma_schemas import ParaTeamMatchParsing
from api.service import team_match_parsing
from api.util.marshmallow_tools import validate_ma

log = logging.getLogger(__name__)


class ParseTeamMatch(Resource):

    @validate_ma(ParaTeamMatchParsing)
    def post(self):
        para = g.req_para
        log.info(u'Receive request to parser match from para={}'.format(para))
        try:
            return team_match_parsing(para['url'])
        except ConnectionError as e:
            return {'message': 'Errors occured during process', u'error': str(e)}, 500
