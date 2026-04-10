#!/usr/bin/python3

import glob
import os
import subprocess

from colorclass import Color
from debian.deb822 import PkgRelation
from terminaltables3 import SingleTable


class Binary:
    '''some binary artefact'''
    filename: str
    arch: str
    buster: bool = False
    trixie: bool = False

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.arch = filename.split('_')[2].split('.')[0]

    def deploy(self) -> None:
        '''is this package relevant for Buster ? for Trixie ?'''
        self.buster = True
        self.trixie = True

        depends = subprocess.check_output(['dpkg-deb', '--field', self.filename, 'Depends'],
                                           text=True).strip('\n ')

        if not depends:
            return
        parser = PkgRelation()
        for rel in parser.parse_relations(depends):
            for rel_item in rel:
                if rel_item['name'] == 'base-files':
                    operator, version = rel_item['version']
                    if operator == '>>':
                        self.buster = False
                    else:
                        self.trixie = False


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
        assert len(self.binaries) in (1, 2)
        if 'all' in self.binaries:
            assert len(self.binaries) == 1

        for binary in self.binaries:
            if len(self.binaries) == 1:
                binary.deploy()
            elif binary.arch == 'amd64':
                binary.trixie = True
            else:
                binary.buster = True


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

def tick(flag: bool) -> str:
    if flag:
        return Color('{autogreen}✓{/autogreen}')
    else:
        return Color('{autored}✗{/autored}')

def deploy():
    '''cute deployement'''
    packages = Packages()
    packages.scan()
    packages.deploy()
    data = [['package', 'arch', 'buster', 'trixie']]
    for package in packages.packages.values():
        for binary in package.binaries:
            data.append([package.name, binary.arch, tick(binary.buster), tick(binary.trixie)])
    render = SingleTable(data, 'Sorting Hat')
    print(render.table)

deploy()
