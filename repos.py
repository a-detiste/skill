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


class Binary:
    '''some binary artefact'''
    filename: str
    arch: str
    buster: bool = False
    trixie: bool = False

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

    def deploy(self) -> None:
        '''run deployment'''
        assert self.binaries
        if len(self.binaries) == 2:
            for binary in self.binaries:
                if binary.arch == 'amd64':
                    binary.trixie = True
                else:
                    binary.buster = True
        else:
            binary = list(self.binaries)[0]
            depends = subprocess.check_output(['dpkg-deb', '--field', binary.filename, 'Depends'],
                                              text=True).strip('\n ')

            binary.buster, binary.trixie = relevant(depends)

class Packages:
    '''all the packages'''
    packages: dict[str, Package] = dict()

    def scan(self) -> None:
        '''scan all the *deb files, get one or two .deb per package'''
        for p in sorted(glob.glob('*.deb')):
            basename = os.path.basename(p)
            name = basename.split('_')[0]
            if name not in self.packages:
                self.packages[name] = Package(name)
            binary = Binary(p)
            self.packages[name].add(binary)

    def deploy(self) -> None:
        for package in self.packages.values():
            package.deploy()


def deploy():
    packages = Packages()
    packages.scan()
    packages.deploy()
    data = list()
    for package in packages.packages.values():
        for binary in package.binaries:
            data.append([package.name, binary.arch, binary.buster, binary.trixie])
    return data


def tick(flag: bool) -> str:
    if flag:
        return Color('{autogreen}✓{/autogreen}')
    else:
        return Color('{autored}✗{/autored}')


def table():
    table_data = [['package', 'arch', 'buster', 'trixie']]
    for r in deploy():
        table_data.append([r[0], r[1], tick(r[2]), tick(r[3])])
    render = SingleTable(table_data, 'Sorting Hat')
    print(render.table)

table()
