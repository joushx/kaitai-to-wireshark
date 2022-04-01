from jinja2 import Environment, FileSystemLoader

class WiresharkGenerator:
    def __init__(self, description):
        self.description = description

    def generate(self):
        env = Environment(loader=FileSystemLoader("generate/templates/"), trim_blocks=True, lstrip_blocks=True)
        #env.filters["field_name"] = field_name
        #env.filters["field_title"] = field_title
        #env.filters["wireshark_type"] = wireshark_type
        #env.filters["size"] = size

        # load template
        template = env.get_template("main.j2")

        # generate result
        return template.render(d=self.description)