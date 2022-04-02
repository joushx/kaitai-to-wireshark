PRIMITIVES = ["u1", "u2", "u4", "str"]

def is_primitive(field):
    if field["type"] in PRIMITIVES:
        return True

    if field["type"] is None and field["size"] != None:
        return True

    if "contents" in field and field["contents"] != None:
        return True

    return False

def get_wireshark_type(value):
    if value == "u1":
        return "uint8"
    elif value == "u2":
        return "uint16"
    elif value == "u4":
        return "uint32"
    else:
        return "bytes"

def calculate_size(field):
    if "size" in field  and field["size"] != None:
        return field["size"]

    if "contents" in field and field["contents"] != None:
        return len(field["contents"])

    if field["type"] == "u1":
        return 1
    elif field["type"] == "u2":
        return 2
    elif field["type"] == "u4":
        return 4
    else:
        return None