PRIMITIVES = ["u1", "u2", "u2be", "u2le", "u4", "u4be", "u4le", "u8", "u8be", "u8le", "s1", "s2", "s2le", "s2be", "s4", "s4be", "s4le", "s8", "s8le", "s8be", "str"]
TYPES = {
    "u1": "uint8",
    "u2": "uint16",
    "u2le": "uint16",
    "u2be": "uint16",
    "u4": "uint32",
    "u4le": "uint32",
    "u4be": "uint32",
    "u8": "uint64",
    "u8le": "uint64",
    "u8be": "uint64",
    "s1": "int8",
    "s2": "int16",
    "s2le": "uint16",
    "s2be": "uint16",
    "s4": "int32",
    "s4le": "int32",
    "s4be": "int32",
    "s8": "int64",
    "s8le": "int64",
    "s8be": "int64",
    "str": "string"
}

def is_primitive(field):
    if field["type"] in PRIMITIVES:
        return True

    if field["type"] is None and field["size"] != None:
        return True

    if "contents" in field and field["contents"] != None:
        return True

    if field["type"] is None and field["value"] != None:
        return True

    return False

def get_wireshark_type(value):
    

    if value in TYPES:
        return TYPES[value]
    elif value == None:
        return "bytes"
    else:
        print("Unknown type: " + str(value))
        return "bytes"

def get_add_fn(type, default_endianess):
    """
    >>> get_add_fn("u2", None)
    'add'
    """
    if type[-2:] == "le":
        return "add_le"
    elif type[-2:] == "be":
        return "add"
    elif default_endianess == "le":
        return "add_le"
    else:
        return "add"

def calculate_size(field):
    if "size" in field and field["size"] != None:
        if type(field["size"]) == int:
            return field["size"]
        else:
            return "values[\"" + field["size"] + "\"]"
    

    if "contents" in field and field["contents"] != None:
        return len(field["contents"])

    if field["type"] is None and "value" in field and field["value"] != None:
        return 0 #  TODO implement value calculation in lua

    t = field["type"]
    if t == "u1" or t == "s1":
        return 1
    elif t == "u2" or t == "u2le" or t == "u2be" or t == "s2" or t == "s2le" or t == "s2be":
        return 2
    elif t == "u4" or t == "u4le" or t == "u4be" or t == "s4" or t == "s4le" or t == "s4be":
        return 4
    elif t == "u8" or t == "u8le" or t == "u8be" or t == "s8" or t == "s8le" or t == "s8be":
        return 8
    else:
        print("Unknown size: " + str(type))
        return None

def get_value_fn(type, default_endianess):
    # TODO does not cover all cases

    if type == "str":
        return ":string()"
    elif (default_endianess == "be" or default_endianess is None) and (type == "u1" or type == "u2" or type == "u4"):
        return ":uint()"
    elif type == "u1be" or type == "u2be" or type == "u2be":
        return ":uint()"
    elif type == "u8be":
        return ":uint64()"
    else:
        return ":tohex()"