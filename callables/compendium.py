'''
All functions related to parsing AHRQ website for data

author: Derek Herincx (derek663@gmail.com)
last_updated: 12/04/2020
'''

from typing import Pattern

import re
import urllib.request
import requests

from bs4 import BeautifulSoup

from config import Config as cfg
from errors.exceptions import MissingHrefError, Error404

# regular expressions compiled here for efficiency
CSV_REGEX = re.compile(".csv$")
HREF_REGEX = re.compile("compendium-([0-9]{4})")

class Parser:
    """
    Generalized Parser class

    Args:
        url (str): a URL string
    """
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def is_response_valid(response):
        """
        Does GET request return a valid response (status code of 200)?

        Args:
            response: A Response object

        Returns:
            bool: True or False
        """
        return response.status_code == 200


    def create_soup_from_url(self, parser: str = 'html.parser'):
        """
        Creates a soup object from a valid URL

        Args:
            - url (str): A URL string
            - parser (str, default: 'html.parser'): Type of parser to use with bs4

        Raises:
            - Error404: 404 Error custom class

        Returns:
        - soup (bs4.BeautifulSoup) - A bs4 soup object to extract info from
        """

        response = requests.get(self.url, timeout=10)

        if self.is_response_valid(response):
            text = response.text
            soup = BeautifulSoup(text, parser)
        else:
            raise Error404(msg="404 Error. Check that the URL is valid.")
        return soup


    @staticmethod
    def parse_soup_for_regex_matches(soup, pattern: Pattern[str]):
        """
        Parses a bs4.BeautifulSoup object and finds href objects matching the
        compiled regex pattern

        Args:
            - soup (bs4.BeautfiulSoup): a beautiful soup object
            - pattern (re.Pattern): a compiled regex object
                * Example: re.compile("[0-9]")

        Returns:
            - hrefs (list): Matching href objects

        """
        hrefs = soup.find_all(href=pattern)
        return hrefs


class Compendium(Parser):
    """
    Class pertaining to AHRQ compendium files
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _AHRQ_COMPENDIUM_BASE(self):
        return "https://www.ahrq.gov/chsp/data-resources/compendium"

    def get_href_links(self, pattern: Pattern[str]) -> list:
        """
        AHRQ's page contains data within the `href` attribute. This method
        takes a soup object and retrieves `href` values that match a specific
        regex pattern

        Args:
            - pattern (Pattern[str]): a compiled regex object
                * Example: re.compile("[0-9]")

        Raises:
            - MissingHrefError (Exception): custom error from the
            `errors.exceptions` module if soup object is parsed and no
            compendium hrefs are found

        Returns:
            - hrefs (list): list of hrefs matching regex pattern

        """

        soup = self.create_soup_from_url()

         # ideally, retrieves a small set of hrefs linking to data
        hrefs = self.parse_soup_for_regex_matches(soup=soup, pattern=pattern)
        if not hrefs:
            raise MissingHrefError

        # cleanup to retrieve href value, not entire tag
        hrefs = [h['href'] for h in hrefs]
        return hrefs

    def create_valid_data_urls(
        self,
        pattern: Pattern[str] = HREF_REGEX
    ) -> list:
        """
        Small utility function that creates a proper, url string from
        the extracted `href` text for each compendium year

        Args:
            - pattern (Pattern[str]): a compiled regex object
                * Example: re.compile("[0-9]")

        Returns:
            - valid_urls (list): urls that contain the AHRQ's base URL string
        """

        valid_urls = []
        for href in self.get_href_links(pattern):
            # use the same regex pattern, but access second group match
            year = re.search(pattern, href).group(1)
            valid_urls.append(f"{self._AHRQ_COMPENDIUM_BASE}-{year}.html")

        return valid_urls


if __name__ == '__main__':
    parser = Compendium(cfg.AHRQ_COMPENDIUM_URL)
    urls = parser.create_valid_data_urls()

    # gets us the files to download
    file_urls = [Compendium(url).get_href_links(CSV_REGEX) for url in urls]
