from jinja2 import Environment, FileSystemLoader

class WiresharkGenerator:
    """
    Generates a wireshark lua dissector from the intermediate format
    """

    def __init__(self, description):
        self.description = description

    def generate(self):
        env = Environment(
            loader=FileSystemLoader("generate/templates/"),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # load template
        template = env.get_template("main.j2")

        # generate result
        return template.render(d=self.description)
