'''
This code is inspired and slightly modified from
https://github.com/PrefectHQ/prefect/blob/master/src/prefect/configuration.py

author: derek663@gmail.com
last_updated: 10/18/2020
'''
class CompoundKey(tuple):
    pass

def nested_to_flatdict(dct: dict, parent=None):
    """
    Converts a nested dictionary into a flattened representation. Nested keys
    will be represented as a CompoundKey (i.e. tuple)

    Args:
        - dct (dictionary): a Python dictionary object
    """
    key_tuples = []
    k_parent = parent or tuple()
    for k,v in dct.items():
        parent_key = CompoundKey(k_parent + (k,))
        if isinstance(v, dict):
            # since flatten_dict() returns a list, we need to use `extend`
            # to add items from the list and not the list itself

            # Note: we use .items() since applying extend to a dict will only
            # extend a dict's keys.
            key_tuples.extend(nested_to_flatdict(v, parent_key).items())
        else:
            key_tuples.append((parent_key, v))
    return dict(key_tuples)
