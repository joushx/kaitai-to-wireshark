from utils.names import for_human
from utils.types import is_primitive, calculate_size, get_wireshark_type
from transpile.field_extractor import FieldExtractor

class KaitaiToWiresharkTranspiler:
    def __init__(self, definition):
        self.definition = definition
        self.result = {}

    def process(self):
        self._generate_names()
        self._generate_fields()
        self._add_sizes()
        self._add_variable_names()
        self._add_data_types()

    def _generate_names(self):
        self.result["names"] = {
            "proto": "{}_proto".format(self.definition["meta"]["id"]),
            "dissector_id": self.definition["meta"]["id"],
            "dissector_name": for_human(self.definition["meta"]["id"]),
            "filename": "{}.lua".format(self.definition["meta"]["id"]),
        }

    def _generate_fields(self):
        fields = FieldExtractor(self.definition).extract()

        self.result["fields"] = {}
        self.result["fields"]["primitive"] = list(filter(lambda item: is_primitive(item), fields))
        self.result["fields"]["complex"] = list(filter(lambda item: not is_primitive(item), fields))
        self.result["fields"]["root"] = list(filter(lambda item: len(item["path"]) == 0, fields)) # TODO add info if root items are primitive or not

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

    def _add_data_types(self):
        for i in range(len(self.result["fields"]["primitive"])):
            field = self.result["fields"]["primitive"][i]
            data_type = get_wireshark_type(field["type"])
            self.result["fields"]["primitive"][i]["wireshark_type"] = data_type