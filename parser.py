import os
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
    _validators: dict

    def __init__(self, validators: dict, schema):
        self.set_validators(validators)
        self._schema = schema

    def parse(self, file):
        with open(file, 'r') as f:
            xml = f.read()
        root = etree.fromstring(xml)
        self._parse(root)

    def _parse(self, root: etree.Element):
        if root.tag in self._validators.keys():
            self._validators[root.tag].validate(root)
        else:
            print(f'Not found tag - {root.tag}')
        for elem in root.getchildren():
            self._parse(elem)

    def set_validators(self, validators):
        self._validators = validators.copy()


class KRSUParser(Parser):
    pass


class Node:
    @classmethod
    def validate(cls, node):
        print(f'<{cls.__name__}> {node.tag} {node.text!r} {node.attrib}')


class TextNode(Node):
    pass


class IntNode(TextNode):
    @classmethod
    def validate(cls, node):
        if not node.text.isdigit():
            print(f'--- ({node.tag}) <{node.text!r}> not integer')


class FileNode(Node):
    @classmethod
    def validate(cls, node):
        if not os.path.isfile(node.text):
            print(f'--- {node.text} not exists')


class CheckerNode(FileNode):
    pass


class GroupNode(Node):
    pass


types = {
    'krsu': KRSUParser({
        'testinfo': Node,
        'checker': FileNode,
        'interactor': FileNode,
        'problem': FileNode,
        'memorylimit': IntNode,
        'timelimit': IntNode,
        'testversion': IntNode,
        'group': GroupNode,
    }, 'krsu.xsd'),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', '-t', choices=types.keys(), help='Parser type')
    parser.add_argument('--file', '-f', help='Main xml file')
    args = parser.parse_args()
    args.type = 'krsu'
    args.file = 'testinfo.xml'
    cls = types[args.type]
    cls.parse(args.file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
