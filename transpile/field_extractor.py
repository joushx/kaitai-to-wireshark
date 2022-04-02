class FieldExtractor:
    def __init__(self, definition):
        self.definition = definition

    def _collect_sequence_fields(self) -> []:
        def build_field(item):
            return {
                "id": item["id"], 
                "type": item["type"] if "type" in item else None, 
                "size": item["size"] if "size" in item else None,
                "contents": item["contents"] if "contents" in item else None, 
                "path": []
            }

        if "seq" not in self.definition:
            return []
        return list(map(build_field, self.definition["seq"]
        ))

    def _collect_type_fields(self, type_name: str) -> []:
        def build_field(item):
            return {
                "id": item["id"], 
                "type": item["type"] if "type" in item else None, 
                "size": item["size"] if "size" in item else None,
                "contents": item["contents"] if "contents" in item else None,
                "path": [type_name]
            }
        return list(map(build_field, self.definition["types"][type_name]["seq"]))

    def _collect_types_fields(self) -> []:
        fields = []
        if "types" not in self.definition:
            return []
        for type_name in self.definition["types"]:
            fields.extend(self._collect_type_fields(type_name))
        return fields

    def _collect_instance_fields(self) -> []:
        fields = []
        if "instances" not in self.definition:
            return []
        for instance_name in self.definition["instances"]:
            instance = self.definition["instances"][instance_name]
            fields.append({
                "id": instance_name, 
                "type": instance["type"] if "type" in instance else None, 
                "size": instance["size"] if "size" in instance else None,
                "contents": instance["contents"] if "contents" in instance else None,
                "pos": instance["pos"] if "pos" in instance else None,
                "path": []
            })
        return fields

    def extract(self) -> []:
        result = self._collect_sequence_fields()
        result.extend(self._collect_types_fields())
        result.extend(self._collect_instance_fields())

        return result