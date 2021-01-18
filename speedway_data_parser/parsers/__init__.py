import logging
from urllib.parse import urlparse

from speedway_data_parser.parsers import speedway_ekstraliga_parser

log = logging.getLogger(__name__)

dct_parser_by_url = {
    u'speedwayekstraliga.pl': speedway_ekstraliga_parser.TeamMatchParser,
    u'www.speedwayekstraliga.pl': speedway_ekstraliga_parser.TeamMatchParser,
}


class TeamMatchParserBuilder():
    @staticmethod
    def by_url(url):
        url_obj = urlparse(url)
        parser_cls = dct_parser_by_url.get(url_obj.netloc)
        if not parser_cls:
            raise ValueError(u'Compatible parser not found for url={}'.format(url))
        log.debug(u'Parser {} was created'.format(parser_cls))
        return parser_cls()
