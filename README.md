# healthcare-airflow
A first dive into Airflow for the public healthcare API


## Parsing the AHRQ site
The first step in retrieving data from the AHRQ site is to be able to parse the site's relatively simple nested structure in order to retrieve two distinct `csv` files across multiple years. Python's `BeautifulSoup` module has made it easy to traverse HTML structures and retrieve very specific tags. Despite this seemingly easy request, data appears to get uploaded to the AHRQ site on a bi-yearly basis so in order to ensure we pull all data regardless of the _current_ status of the site, we must use a combination of regular expressions and HTML parsing to fulfill our request. 


### Parser
The `Parser` class is meant to work in isolation for any URL string:

```python3

import re
from compendium import Parser

# Instantiating a parser for AHRQ's main compendium page
url = "https://www.ahrq.gov/chsp/data-resources/compendium.html"
parser = Parser(url=url)

# Creating a bs4 soup object
soup = parser.create_soup_from_url()

# searches entire `soup` for strings matching `pattern` in `href` attributes
# use the `name` parameter to search other attributes
matches = parser.parse_soup_for_regex_matches(
  soup,
  pattern=re.compile("compendium-([0-9]{4})")
)


# matches = [
#  <a href="/chsp/data-resources/compendium-2018.html">2018 Compendium</a>,
#  <a href="/chsp/data-resources/compendium-2016.html">2016 Compendium</a>
# ]

```
