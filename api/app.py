import logging
import logging.config

import simplejson
from flask import Flask, make_response
from flask_restful import Api

from api.util.json_util import json_encoder


class ParserApp(Flask):
    def __init__(self, config, name='parser_app', *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.config.from_object(config)

    def add_logging_handlers(self):
        from api.logging_config import LOGGING_CONFIG
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger = logging.getLogger(__name__)
        self.logger.info(u'Logging initialized')

    def add_flask_restful(self):
        self.logger.info('Initializing flask_restul')
        api = Api(self)

        @api.representation('application/json')
        def output_json(data, code, headers=None):
            resp = make_response(simplejson.dumps(data, default=json_encoder), code)
            resp.headers.extend(headers or {})
            return resp

        return api

    def add_marshmallow(self):
        from flask_marshmallow import Marshmallow
        ma = Marshmallow(self)
        return ma

    def init_resources(self, api):
        self.logger.info(u'Initializing resources')
        from api.resources import ParseSeasonMatches, ParseTeam, ParseTeamMatch
        api.add_resource(ParseTeamMatch, '/parser/team_match_parsing')
        api.add_resource(ParseTeam, '/parser/team_parsing')
        api.add_resource(ParseSeasonMatches, '/parser/season_matches')


def create_app(*args, **kwargs):
    app = ParserApp(*args, **kwargs)
    app.add_logging_handlers()
    app.add_marshmallow()
    api = app.add_flask_restful()
    app.init_resources(api)

    return app
