import logging

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from speedway_data_parser.interpreters import ParsedTeamMatchInterpreter
from speedway_data_parser.parsers import (SeasonMatchesParserBuilder,
                                          TeamMatchParserBuilder,
                                          TeamParserBuilder)

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


def team_parsing(url):
    log.info('Do request to url={}'.format(url))
    ret = requests.get(url)
    parser = TeamParserBuilder.by_url(url)
    parser.parse(ret.text)
    return {
        'name': parser.get_team_name(),
        'year': parser.get_year(),
        'riders': parser.get_team_members(),
    }


def set_chrome_options() -> None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def season_matches_parsing(season):
    log.info('Get matches links for season=%r', season)
    parser = SeasonMatchesParserBuilder.by_name('ekstraliga')
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get('https://speedwayekstraliga.pl/terminarz-i-wyniki/pge-ekstraliga/?y={}'.format(season))
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'schedule__grid')))
    with open('./test', 'w') as f:
        f.write(driver.page_source)
    parser.parse(driver.page_source)
    driver.close()
    return {
        'matches_links': parser.get_match_links(),
    }
