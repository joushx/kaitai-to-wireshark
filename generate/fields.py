def collect_sequence_fields(data: dict) -> []:
    return list(map(lambda item: {"id": item["id"], "type": item["type"] if "type" in item else None, "size": item["size"] if "size" in item else None, "path": []}, data["seq"]))

def collect_type_fields(data: dict, type_name: str) -> []:
    return list(map(lambda item: {"id": item["id"], "type": item["type"] if "type" in item else None, "size": item["size"] if "size" in item else None, "path": [type_name]}, data["types"][type_name]["seq"]))

def collect_types_fields(data: dict) -> []:
    fields = []
    for type_name in data["types"]:
        fields.extend(collect_type_fields(data, type_name))
    return fields

def collect_fields(data: dict) -> []:
    result = collect_sequence_fields(data)
    result.extend(collect_types_fields(data))

    return result