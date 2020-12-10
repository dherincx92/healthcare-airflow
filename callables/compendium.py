'''
Class objects related to parsing a webpage and the AHRQ site.

author: Derek Herincx (derek663@gmail.com)
last_updated: 12/10/2020
'''

from typing import Pattern

import re
import requests

from bs4 import BeautifulSoup

from errors.exceptions import MissingHrefError, Error404
from utilities.urls import URL

# regular expressions compiled here for efficiency
CSV_REGEX = re.compile(".csv$")
HREF_REGEX = re.compile("compendium-([0-9]{4})")
re_options = {"csv": CSV_REGEX, "href": HREF_REGEX}

# Type hints
Response = requests.models.Response
soup = BeautifulSoup

class Parser:
    """
    Parser class. Object is generalized to be instantiated with any URL. Users
    can call the `create_soup_from_url` method to view a BeautifulSoup object
    resulting from theirHTTP request. This class also enables a user to parse
    any soup object and find href attributes matching a specifc regex pattern

    Args:
        url (str): a URL string
    """
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def is_response_valid(response: Response) -> bool:
        """
        Does GET request return a valid response (status code of 200)?

        Args:
            - response (requests.models.Response): A Response object

        Returns:
            - bool: True or False
        """
        return response.status_code == 200


    def create_soup_from_url(self, parser: str = 'html.parser') -> soup:
        """
        Creates a soup object from a valid URL

        Args:
            - url (str): A URL string
            - parser (str, default: 'html.parser'): Type of parser to use with bs4

        Raises:
            - Error404 (errors.exceptions): 404 Error custom class

        Returns:
            - soup (bs4.BeautifulSoup): A bs4 soup object to extract info from
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
    Inherits from Parser and contains specific methods pertaining to retrieving
    compendium files from `https://www.ahrq.gov`. This class uses methods
    inherited from Parser to retrieve appropriate href links to multi-year
    compendium files. Due to inconsistencies in href links from AHRQ, this
    class performs small string manipulations to output proper URLs and ensure
    things like domain are included

    Inherits:
        - Parser (object)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def AHRQ_COMPENDIUM_DOMAIN(self) -> str:
        return "https://www.ahrq.gov/"

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
            raise MissingHrefError("No tags matching tags were found")

        # cleanup to retrieve href value, not entire tag
        hrefs = [h['href'] for h in hrefs]
        return hrefs

    def create_formatted_regex_urls(
        self,
        pattern: str,
    ) -> list:
        """
        Small utility function that creates a proper, url string from
        the extracted `href` text for each compendium year

        Args:
            - pattern (str): either specify "csv" or "href" to indicate you
            want to find csv files or compendium links.

        Returns:
            - valid_urls (list): urls that contain the AHRQ's base URL string
        """
        options = list(re_options.keys())
        if pattern not in options:
            msg = ' or '.join(options)
            raise ValueError(f"pattern must be a string: either {msg}")

        valid_urls = []
        # formatter to make valid URLs
        formatter = URL(self.AHRQ_COMPENDIUM_DOMAIN)

        for href in self.get_href_links(re_options[pattern]):
            valid_urls.append(formatter.configure(href))

        return valid_urls
