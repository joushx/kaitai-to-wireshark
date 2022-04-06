from utils.names import for_human
from utils.types import is_primitive, calculate_size, get_wireshark_type, get_add_fn, get_value_fn
from transpile.field_extractor import FieldExtractor

class KaitaiToWiresharkTranspiler:
    """
    Generate immediate representation from the input
    """
    def __init__(self, definition):
        self.definition = definition
        self.result = {}

    def process(self):
        self._generate_names()
        self._generate_fields()
        self._add_sizes()
        self._add_variable_names()
        self._add_filter_names()
        self._add_function_names()
        self._add_data_types()
        self._add_settings()

    def _generate_names(self):
        self.result["names"] = {
            "proto": "{}_proto".format(self.definition["meta"]["id"]),
            "dissector_id": self.definition["meta"]["id"],
            "dissector_name": for_human(self.definition["meta"]["id"]),
            "filename": "{}.lua".format(self.definition["meta"]["id"]),
        }

    def _generate_fields(self):
        fields = FieldExtractor(self.definition).extract()

        for field in fields:
            field["title"] = for_human(field["id"])
            field["primitive"] = is_primitive(field)

        self.result["fields"] = {}
        self.result["fields"]["primitive"] = list(filter(lambda item: item["primitive"], fields))
        self.result["fields"]["complex"] = list(filter(lambda item: not item["primitive"], fields))
        self.result["fields"]["root"] = list(filter(lambda item: len(item["path"]) == 0, fields))
        self.result["fields"]["type"] = self._group_by_path(fields)

    def _add_sizes(self):
        for i in range(len(self.result["fields"]["primitive"])):
            field = self.result["fields"]["primitive"][i]
            size = calculate_size(field)
            self.result["fields"]["primitive"][i]["size"] = size

    def _add_variable_names(self):
        for i in range(len(self.result["fields"]["primitive"])):
            field = self.result["fields"]["primitive"][i]
            path = "_".join(field["path"])
            if len(path) > 0:
                path = path + "_"
            variable = "f_" + path + field["id"]
            self.result["fields"]["primitive"][i]["variable"] = variable

    def _add_filter_names(self):
        for i in range(len(self.result["fields"]["primitive"])):
            field = self.result["fields"]["primitive"][i]
            path = ".".join(field["path"])
            if len(path) > 0:
                path = path + "."
            filter_value = self.result["names"]["dissector_id"] + "." + path + field["id"]
            self.result["fields"]["primitive"][i]["filter"] = filter_value

    def _add_function_names(self):
        for i in range(len(self.result["fields"]["complex"])):
            field = self.result["fields"]["complex"][i]
            path = "_".join(field["path"])
            if len(path) > 0:
                path = path + "_"
            function_name = "dissect_" + path + field["type"]
            self.result["fields"]["complex"][i]["function"] = function_name

    def _add_data_types(self):
        for i in range(len(self.result["fields"]["primitive"])):
            field = self.result["fields"]["primitive"][i]
            data_type = get_wireshark_type(field["type"])
            self.result["fields"]["primitive"][i]["wireshark_type"] = data_type
            self.result["fields"]["primitive"][i]["add_fn"] = get_add_fn(data_type, self.definition["meta"]["endian"] if "endian" in self.definition["meta"] else None)
            self.result["fields"]["primitive"][i]["value_fn"] = get_value_fn(field["type"], self.definition["meta"]["endian"] if "endian" in self.definition["meta"] else None)

    def _group_by_path(self, fields):
        groups = {}

        for field in fields:

            # no root fields
            if len(field["path"]) == 0:
                continue

            if field["path"][0] not in groups:
                groups[field["path"][0]] = []

            groups[field["path"][0]].append(field)

        return groups

    def _add_settings(self):
        self.result["settings"] = {}
        self.result["settings"]["add"] = "add_le" if ("endian" in self.definition["meta"] and self.definition["meta"]["endian"] == "le") else "add"
