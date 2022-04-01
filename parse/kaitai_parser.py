from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class KaitaiParser:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        definition_file = open(self.filename).read()
        return load(definition_file, Loader=Loader)