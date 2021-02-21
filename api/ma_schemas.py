from marshmallow import Schema

from api.util.marshmallow_tools import req_url


class ParaTeamMatchParsing(Schema):
    url = req_url()


class ParaTeamParsing(Schema):
    url = req_url()
