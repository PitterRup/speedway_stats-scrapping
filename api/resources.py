import logging

from flask import g
from flask_restful import Resource

from api.ma_schemas import ParaTeamMatchParsing
from api.util.marshmallow_tools import validate_ma

log = logging.getLogger(__name__)


class ParseTeamMatch(Resource):

    @validate_ma(ParaTeamMatchParsing)
    def post(self):
        para = g.req_para
        return para
