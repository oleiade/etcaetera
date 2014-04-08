from etcaetera.exceptions import MalformationError


def format_key(key):
    return key.strip().upper().replace(' ', '_')


def is_nested_key(key):
    if (key.startswith('.') or
        key.endswith('.') or
        '..' in key):
        raise MalformationError 

    return '.' in key
