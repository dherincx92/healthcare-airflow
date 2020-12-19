'''
Configuration class to parse a toml file

author: derek663@gmail.com
last_updated: 12/18/2020
'''

from ast import literal_eval
from os.path import dirname, join
import re

import toml
from box import Box

from app.utilities import nested_to_flatdict
from app.errors import ItemNotFound

INTERPOLATION_REGEX = re.compile(r"(\${(.[^${}]*)})")
DEFAULT_CONFIG = join(dirname(__file__), "config.toml")

def literal_value_conversion(val: str):
    """
    Applies literal expression conversion to parsed objects from a TOML
    configuration file. Booleans, regardless of case, will be handled properly

    Args:
        - val (str): a string object to be converted

    Returns:
        - val (str): a string parsed into its literal Python type
    """
    try:
        val = literal_eval(val)
    except ValueError:
        pass
    return val

def load_toml(path: str):
    """
    Loads configuration from a TOML file
    """
    return {
        k: literal_value_conversion(v) for k,v in toml.load(path).items()
    }

def interpolate_config_vars(config, val: str):
    """
    Interpolates and formats strings referencing other keys in our TOML file.
    While this isn't default behavior for TOML, we enable it here to reduce
    string duplication where possible

    Args:
        - config (dict): a dictionary type
        - val (str): a string to format
    """

    # matches is a list of tuples; each tuple contain 2 groups from regex pattern
    matches = re.findall(INTERPOLATION_REGEX, val)

    for match in matches:
        match_tuple = tuple(match[1].split("."),)
        if not match_tuple in dct.keys():
            raise ItemNotFound(f"""
                Attempting to substitute {match[1]} in your TOML config file but
                it seems that key is not found
            """)
        else:
            val = val.replace(match[0], dct[match_tuple])
        return val

def load_configuration(path: str):
    default_config = load_toml(path)

    # flattened dictionary for easier parsing
    flat_config = nested_to_flatdict(default_config)




config = load_configuration(DEFAULT_CONFIG)





