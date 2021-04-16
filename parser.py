#!/usr/bin/env python
import os
import sys
import argparse
from lxml import etree

from io import StringIO


class Parser:
    _validators: dict

    def __init__(self, validators: dict):
        self.set_validators(validators)

    def parse(self, file):
        pass

    def set_validators(self, validators):
        self._validators = validators.copy()


class XMLParser(Parser):
    _schema: str

    def __init__(self, validators: dict):
        super().__init__(validators)
        self.schema = etree.XMLSchema(etree.parse(self._schema))

    def parse(self, file):
        with open(file, 'r') as f:
            xml = f.read()

        root = etree.fromstring(xml)
        self.schema.validate(etree.parse(StringIO(xml)))
        self._parse(root)

    def _parse(self, root: etree.Element):
        if root.tag in self._validators.keys():
            self._validators[root.tag].validate(root)
        else:
            print(f'Not found tag - {root.tag}')
        for elem in root.getchildren():
            self._parse(elem)


class KRSUParser(XMLParser):
    _schema = 'krsu.xsd'


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
            print(f'--- ({node.tag}) <{node.text!r}> not integer'.center(os.get_terminal_size()[0]//2))


class FileNode(Node):
    @classmethod
    def validate(cls, node):
        if not os.path.isfile(node.text):
            print(f'--- {node.text} not exists')


class CheckerNode(FileNode):
    pass


class GroupNode(Node):
    pass


class TestNode(Node):
    @classmethod
    def validate(cls, node):
        _input = node.get('input')
        _output = node.get('output')
        cls.file_exists(_input)
        cls.file_exists(_output)

    @classmethod
    def file_exists(cls, path):
        if not os.path.isfile(path):
            print(f'--- {path} not exists')


types = {
    'krsu': KRSUParser({
        'checker': FileNode,
        'interactor': FileNode,
        'problem': FileNode,
        'runtype': IntNode,
        'memorylimit': IntNode,
        'timelimit': IntNode,
        'testversion': IntNode,
        'group': GroupNode,
        'test': TestNode,
    }),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', '-t', choices=types.keys(), help='Parser type', default='krsu')
    parser.add_argument('--file', '-f', help='Main xml file', default='testinfo.xml')
    args = parser.parse_args()
    cls = types[args.type]
    cls.parse(args.file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
