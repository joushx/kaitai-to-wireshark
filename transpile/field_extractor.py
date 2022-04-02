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
        for type_name in self.definition["types"]:
            fields.extend(self._collect_type_fields(type_name))
        return fields

    def extract(self) -> []:
        result = self._collect_sequence_fields()
        result.extend(self._collect_types_fields())

        return result