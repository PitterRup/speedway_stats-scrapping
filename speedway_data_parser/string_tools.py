def strip(val):
    if val is None:
        return None
    if val:
        return val.strip()
    return val


def int_or_none(val):
    if val is None:
        return None
    try:
        return int(val)
    except ValueError:
        return None
