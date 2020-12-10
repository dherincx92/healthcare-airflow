'''
Configuration objects

author: derek663@gmail.com
last_updated: 10/05/2020
'''

class Config:
  # Home page for AHRQ
  AHRQ_ROOT_URL = "https://www.ahrq.gov"

  # contains href links to different compendium year data
  AHRQ_COMPENDIUM_BASE="https://www.ahrq.gov/chsp/data-resources/compendium"
  AHRQ_COMPENDIUM_URL=f"{AHRQ_COMPENDIUM_BASE}.html"

  # use string formatting to fill in specific compendium year
  AHRQ_SINGLE_YEAR_COMPENDIUM_STRING_FORMAT="{}-{}.html"