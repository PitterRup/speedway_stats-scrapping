import logging

from flask_restful import Resource

log = logging.getLogger(__name__)


class ParseTeamMatch(Resource):
    def post(self):
        return 'ok'
