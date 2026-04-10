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
                    # sorting hat
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

def get_packages() -> dict[str, set[str]]:
    packages: dict[str, set[str]] = dict()

    for p in sorted(glob.glob('*.deb')):
        basename = os.path.basename(p)
        parts = basename.split('_')
        name = parts[0]
        if name not in packages:
            packages[name] = set()
        arch = parts[2].split('.')[0]
        packages[name].add(arch)
    return packages

table_data = [['package', 'arch', 'buster', 'trixie']]

for package, archs in get_packages().items():
    if len(archs) == 2:
        table_data.append([package, 'i386', tick(True), tick(False)])
        table_data.append([package, 'amd64', tick(False), tick(True)])
    else:
        arch = archs.pop()
        filename = glob.glob('%s*%s.deb' % (package, arch))[0]
        depends = subprocess.check_output(['dpkg-deb', '--field', filename, 'Depends'],
                                           text=True).strip('\n ')

        buster, trixie = relevant(depends)
        table_data.append([package, arch, tick(buster), tick(trixie)])

render = SingleTable(table_data, 'Sorting Hat')
print(render.table)
