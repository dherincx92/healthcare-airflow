'''
Class to generalize formatting of URLs

author: derek_herincx@gallup.com
last_updated: 12/10/2020
'''
import re

class URL:
    """
    Generalized URL class

    Args:
        - domain (str): A domain name to check for, with protocol
    """
    def __init__(self, domain: str):
        self.domain=domain

    def __str__(self):
        return f'<URL {self.domain}>'

    def does_domain_exist(self, string: str) -> bool:
        """
        Does the string contain the URL domain? If considering the
        following URL: "https://www.ahrq.gov/data-resources/compendium.html",
        the `domain` is considered "www.ahrq.gov"

        Args:
            - string (str): a string

        Returns:
            - bool: True or False
        """
        assert isinstance(string, str)
        compiled = re.search(self.domain, string)

        return bool(compiled)

    def configure(self, string: str) -> str:
        """
        Configures a URL string to include protocol and domain (if it does
        not already exist).

        Args:
            - string (str): URL string to format

        Returns:

        """
        if not self.does_domain_exist(string):
            string=f'{self.domain}{string}'
        return string
