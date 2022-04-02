def field_name(value):
    """
    Generates the field name out of the field definition dictionary object

    >>> field_name({"id": "foo", "path": []})
    'foo'

    >>> field_name({"id": "bar", "path": ["foo"]})
    'foo_bar'
    """
    path = "_".join(value["path"])
    if len(path) > 0:
        path = path + "_"

    return path + value["id"]

def field_title(value):
    """
    Generate human readable names from snake case
    
    >>> field_title("foo_bar")
    'Foo bar'

    >>> field_title("header")
    'Header'

    >>> field_title("this_is_a_test")
    'This is a test'
    """

    return value.replace("_", " ").capitalize()

def wireshark_type(value):
    """
    Convert kaitai types to wireshark types

    >>> wireshark_type("u1")
    "uint8"

    >>> wireshark_type("u2")
    "uint16"

    >>> wireshark_type(None)
    "bytes"
    """

    if value == "u1":
        return "uint8"
    elif value == "u2":
        return "uint16"
    elif value == "u4":
        return "uint32"
    else:
        return "bytes"

def size(value, size=None):
    """
    Get the size of a type

    >>> size("u1")
    1

    >>> size("u2")
    2

    >>> size(None, size=5)
    5
    """

    if size:
        return size

    if value == "u1":
        return 1
    elif value == "u2":
        return 2
    elif value == "u4":
        return 4
    else:
        return -1