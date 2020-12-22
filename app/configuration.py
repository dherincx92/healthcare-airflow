'''
Configuration class to parse a toml file

author: derek663@gmail.com
last_updated: 12/18/2020
'''

from ast import literal_eval
from os.path import dirname, join
import re
from typing import Pattern

from box import Box
import toml

from app.utilities import mapping
from app.errors import ItemNotFound

INTERPOLATION_REGEX = re.compile(r"(\${(.[^${}]*)})")
DEFAULT_CONFIG = join(dirname(__file__), "config.toml")

def literal_value_conversion(val: str):
    """
    Applies literal expression conversion to parsed objects from a TOML
    configuration file.

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

def check_for_regex_match(val: str, PATTERN: Pattern[str]) -> bool:
    """
    Is PATTERN found anywhere in a string? We just need to know if there is a
    match. We don't need to know if there are multiple matches since we aren't
    doing the substitution here.

    Args:
        - val (str): string to check for matches
        - pattern (Pattern[str]): a compiled regex pattern (i.e. `re.compile`)

    Returns:
        - bool (bool): `True` if a match is found anywhere in string, else
        `False`
    """
    matches = re.search(PATTERN, val)
    return bool(matches)

def interpolate_config_vars(config: dict, val: str):
    """
    Interpolates and formats strings referencing other keys in our TOML file.
    While this isn't default behavior for TOML, we enable it here to reduce
    string duplication where possible. If a non-existent key is found

    Args:
        - config (dict): a dictionary type
        - val (str): a string to format

    Raises:
        - ItemNotFound (Error): exception indicating that the item you
        attempted to substitute does not exist

    Returns:
        - val (str): string with referenced keys interpolated
    """

    # matches is a list of tuples; match will contain 2 groups
    matches = re.findall(INTERPOLATION_REGEX, val)
    for match in matches:
        match_tuple = tuple(match[1].split("."),)
        if not match_tuple in config.keys():
            raise ItemNotFound(f"""
                Attempting to substitute `{match[1]}` in your TOML config
                file but it seems that key is not found
            """)
        else:
            val = val.replace(match[0], config[match_tuple])
    return val

def load_configuration(path: str) -> Box:
    """
    Callable to load a finalized configuration file

    Args:
        - path (str): path to TOML configuration file

    Returns:
        - final_config (Box): configuration object as a Box object. Box object
        allows user to access dicitonary keys as attributes ("dot" notation).
        This will prove beneficial in the `tasks` subdirectory where the
        config object will come into play.

    """

    # loads and does literal type matching
    default_config = load_toml(path)

    # flattened dictionary for easier parsing; inspired by Prefect!
    flat_config = mapping.nested_to_flatdict(default_config)

    keys = flat_config.keys()
    for key in keys:
        # if key is not a string, then do nothing...
        if not isinstance(flat_config[key], str):
            continue
        else:
            check = check_for_regex_match(flat_config[key], INTERPOLATION_REGEX)
            # only interpolate for those referencing other keys
            if check:
                flat_config[key] = interpolate_config_vars(
                    flat_config,
                    flat_config[key]
                )

    final_config = mapping.flatdict_to_dict(flat_config)

    # convert to box in order to access keys as attributes
    final_config = Box(final_config)
    return final_config

# object to be exported for use in `app`
config = load_configuration(DEFAULT_CONFIG)
