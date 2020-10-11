from lxml import html
from datetime import datetime

from speedway_data_parser.util import catch_exceptions

class Parser():
    def __init__(self, html_string):
        self.tree = html.fromstring(html_string)

    @catch_exceptions(IndexError)
    def get_stadium(self):
        elem = self.tree.find_class('match__header__info')[0].getchildren()[0]
        return elem.text.strip()

    @catch_exceptions(IndexError)
    def get_round(self):
        elem = self.tree.find_class('match__header__info')[0].getchildren()[1]
        return elem.text.strip()

    @catch_exceptions(IndexError)
    def get_match_datetime(self):
        str_date = self.tree.find_class('match__header__datetime')[0].strip()
        return datetime.strptime(str_date, '%d.%m.%Y, %H:%M')

    @catch_exceptions(IndexError)
    def get_referee(self):
        elem = self.tree.find_class('match__header__members')[0].getchildren()[0]
        return elem.text_content().strip().replace('Sędzia\n', '')

    @catch_exceptions(IndexError)
    def get_track_commissioner(self):
        elem = self.tree.find_class('match__header__members')[0].getchildren()[1]
        return elem.text_content().strip().replace('Sędzia\n', '')
