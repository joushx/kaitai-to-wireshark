#!/usr/bin/env python3

import sys
from parse.kaitai_parser import KaitaiParser
from transpile.kaitai_wireshark_transpiler import KaitaiToWiresharkTranspiler
from generate.wireshark_generator import WiresharkGenerator

if __name__ == "__main__":
    parser = KaitaiParser(sys.argv[1])
    definition = parser.parse()
    
    transpiler = KaitaiToWiresharkTranspiler(definition)
    transpiler.process()

    generator = WiresharkGenerator(transpiler.result)
    result = generator.generate()

    print(result)