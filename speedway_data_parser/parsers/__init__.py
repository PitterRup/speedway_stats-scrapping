import logging
from urllib.parse import urlparse

from speedway_data_parser.parsers import speedway_ekstraliga_parser

log = logging.getLogger(__name__)


class TeamMatchParserBuilder():
    dct_parser_by_url = {
        u'speedwayekstraliga.pl': speedway_ekstraliga_parser.TeamMatchParser,
        u'www.speedwayekstraliga.pl': speedway_ekstraliga_parser.TeamMatchParser,
    }

    @classmethod
    def by_url(cls, url):
        url_obj = urlparse(url)
        parser_cls = cls.dct_parser_by_url.get(url_obj.netloc)
        if not parser_cls:
            raise ValueError(u'Compatible parser not found for url={}'.format(url))
        log.debug(u'Parser {} was created'.format(parser_cls))
        return parser_cls()


class TeamParserBuilder():
    dct_parser_by_url = {
        u'speedwayekstraliga.pl': speedway_ekstraliga_parser.TeamParser,
        u'www.speedwayekstraliga.pl': speedway_ekstraliga_parser.TeamParser,
    }

    @classmethod
    def by_url(cls, url):
        url_obj = urlparse(url)
        parser_cls = cls.dct_parser_by_url.get(url_obj.netloc)
        if not parser_cls:
            raise ValueError(u'Compatible parser not found for url={}'.format(url))
        log.debug(u'Parser {} was created'.format(parser_cls))
        return parser_cls(year=int(url_obj.query.replace('y=', '')))


class SeasonMatchesParserBuilder:
    dct_parser_by_name = {
        'ekstraliga': speedway_ekstraliga_parser.SeasonMatchesParser,
    }

    @classmethod
    def by_name(cls, name):
        parser_cls = cls.dct_parser_by_name.get(name)
        if not parser_cls:
            raise ValueError(u'Compatible parser not found for name={}'.format(name))
        log.debug(u'Parser {} was created'.format(parser_cls))
        return parser_cls()
