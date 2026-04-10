#!/usr/bin/python3

import glob
import os
import subprocess

from colorclass import Color
from debian.deb822 import PkgRelation
from terminaltables3 import SingleTable


def relevant(depends: str) -> tuple[bool, bool]:
    '''is this package relevant for Buster ? for Trixie ?'''
    for_buster = True
    for_trixie = True

    if depends:
        parser = PkgRelation()
        for rel in parser.parse_relations(depends):
            for rel_item in rel:
                if rel_item['name'] == 'base-files':
                    operator, version = rel_item['version']
                    if operator == '>>':
                        for_buster = False
                    else:
                        for_trixie = False

    return (for_buster, for_trixie)


def tick(flag: bool) -> str:
    if flag:
        return Color('{autogreen}✓{/autogreen}')
    else:
        return Color('{autored}✗{/autored}')


class Binary:
    '''some binary artefact'''
    filename: str
    arch: str

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.arch = filename.split('_')[2].split('.')[0]


class Package:
    '''one package might have 1 or more binaries'''
    name: str
    binaries = set()

    def __init__(self, name: str) -> None:
        self.name = name
        self.binaries = set()

    def add(self, binary: Binary) -> None:
        self.binaries.add(binary)

def get_packages() -> dict[str, set[str]]:
    '''get one or two .deb per package'''
    packages: dict[str, Package] = dict()

    for p in sorted(glob.glob('*.deb')):
        basename = os.path.basename(p)
        parts = basename.split('_')
        name = parts[0]
        if name not in packages:
            packages[name] = Package(name)
        binary = Binary(p)
        packages[name].add(binary)
    return packages

table_data = [['package', 'arch', 'buster', 'trixie']]

for package in get_packages().values():
    if len(package.binaries) == 2:
        table_data.append([package.name, 'i386', tick(True), tick(False)])
        table_data.append([package.name, 'amd64', tick(False), tick(True)])
    else:
        binary = package.binaries.pop()
        depends = subprocess.check_output(['dpkg-deb', '--field', binary.filename, 'Depends'],
                                           text=True).strip('\n ')

        buster, trixie = relevant(depends)
        table_data.append([package.name, binary.arch, tick(buster), tick(trixie)])

render = SingleTable(table_data, 'Sorting Hat')
print(render.table)
