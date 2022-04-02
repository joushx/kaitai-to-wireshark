PRIMITIVES = ["u1", "u2", "u2be", "u2le", "u4", "u4be", "u4le" "u8", "u8be", "u8le", "s1", "s2", "s4", "s8", "s8le", "str"]
TYPES = {
    "u1": "uint8",
    "u2": "uint16",
    "u4": "uint32",
    "u8": "uint64",
    "s1": "int8",
    "s2": "int16",
    "s4": "int32",
    "s8": "int64",
    "str": "string"
}

def is_primitive(field):
    if field["type"] in PRIMITIVES:
        return True

    if field["type"] is None and field["size"] != None:
        return True

    if "contents" in field and field["contents"] != None:
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

def calculate_size(field):
    if "size" in field  and field["size"] != None:
        return field["size"]

    if "contents" in field and field["contents"] != None:
        return len(field["contents"])

    if field["type"] == "u1" or field["type"] == "s1":
        return 1
    elif field["type"] == "u2" or field["type"] == "s2":
        return 2
    elif field["type"] == "u4" or field["type"] == "s4":
        return 4
    elif field["type"] == "u8" or field["type"] == "s8":
        return 8
    else:
        print("Unknown size: " + str(field))
        return None