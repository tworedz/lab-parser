import sys
import argparse
from lxml import etree


class Loader:
    _file: str

    def __init__(self, schema: str):
        self._schema = etree.XMLSchema(schema)

    def load(self, file):
        self._file = file


class Parser:
    _loader: Loader
    _validators: list

    def __init__(self, validators):
        self.set_validators(validators)

    def parse(self, file):
        pass

    def set_validators(self, validators):
        self._validators = validators


class KRSUParser(Parser):
    pass


class Node:
    def validate(self):
        pass


class TextNode(Node):
    pass


class FileNode(Node):
    pass


class CheckerNode(FileNode):
    def validate(self):
        pass


types = {
    'krsu': KRSUParser,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', '-t', choices=types.keys(), help='Parser type')
    parser.add_argument('--file', '-f', help='Main xml file')
    args = parser.parse_args()
    cls = types[args.type]()
    cls.parse(args.file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
