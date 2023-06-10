__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."


def load_api_key() -> str:
    """
        Global function shared by all class in this package
    """
    with open('../.encrypted.ctx', 'r') as f:
        key = f.read()
    return key
