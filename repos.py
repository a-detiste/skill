#!/usr/bin/python3

import glob
import os
import subprocess

from debian.deb822 import PkgRelation


class Binary:
    '''some binary artefact'''
    filename: str
    arch: str
    buster: bool = False
    trixie: bool = False

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.arch = filename.split('_')[2].split('.')[0]

    def __gt__(self, other: 'Binary') -> bool:
        return self.arch > other.arch

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
                    assert rel_item['version']
                    operator, version = rel_item['version']
                    if operator == '>>':
                        self.buster = False
                    else:
                        self.trixie = False
                    return


class Package:
    '''one package might have 1 or more binaries'''
    name: str
    binaries: set[Binary] = set()

    def __init__(self, name: str) -> None:
        self.name = name
        self.binaries = set()

    def __gt__(self, other: 'Package') -> bool:
        return self.name > other.name

    def add_binary(self, deb: str) -> None:
        self.binaries.add(Binary(deb))

    def deploy(self) -> None:
        '''run deployment'''
        assert len(self.binaries) in (1, 2)
        if 'all' in [b.arch for b in self.binaries]:
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
        for deb in glob.glob('*.deb'):
            name = os.path.basename(deb).split('_')[0]
            if name not in self.packages:
                self.packages[name] = Package(name)
            self.packages[name].add_binary(deb)

    def deploy(self) -> None:
        for package in self.packages.values():
            package.deploy()


def deploy() -> None:
    '''cute deployement'''
    from colorclass import Color
    from terminaltables3 import SingleTable

    OK = Color('{autogreen}✓{/autogreen}') # type: ignore
    KO = Color('{autored}✗{/autored}') # type: ignore

    def tick(flag: bool) -> str:
        return OK if flag else KO

    packages = Packages()
    packages.scan()
    packages.deploy()
    data = [['package', 'arch', 'buster', 'trixie']]
    for package in sorted(packages.packages.values()):
        for binary in sorted(package.binaries):
            data.append([package.name, binary.arch, tick(binary.buster), tick(binary.trixie)])
    render = SingleTable(data, 'Sorting Hat')
    print(render.table)

    for package in sorted(packages.packages.values()):
        for binary in sorted(package.binaries):
            if binary.buster:
                 subprocess.call(['aptly', 'repo', 'add', 'buster', binary.filename])
            if binary.trixie:
                 subprocess.call(['aptly', 'repo', 'add', 'trixie', binary.filename])


if __name__ == "__main__":
    # aptly repo create -architectures="i386" buster
    # aptly repo create -architectures="amd64 i386" trixie
    deploy()
