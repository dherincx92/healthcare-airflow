'''
Script to run Compendium class and get proper URLs

author: derek663@gmail.com
last_updated: 12/22/2020
'''

from app.utilities import Compendium
from app.configuration import config

def main():
    compendium = Compendium(config.ahrq.compendium_url)

    # these are the yearly compendium links; we will then use these to
    # instantiate another instance of `Compendium`
    compendium_urls = compendium.create_formatted_regex_urls('compendium')

    # here we get the actual href links to each csv
    csv_files = [
        Compendium(url).create_formatted_regex_urls('csv')
        for url in compendium_urls
    ]

if __name__ == '__main__':
    main()



