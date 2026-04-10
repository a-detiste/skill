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

table_data = [['package', 'arch', 'buster', 'trixie']]

for p in sorted(glob.glob('*.deb')):
    basename = os.path.basename(p)
    parts = basename.split('_')
    name = parts[0]

    arch = parts[2].split('.')[0]

    depends = subprocess.check_output(['dpkg-deb', '--field', p, 'Depends'],
                                      text=True).strip('\n ')


    buster, trixie = relevant(depends)
    table_data.append([name, arch, tick(buster), tick(trixie)])

render = SingleTable(table_data, 'Sorting Hat')
print(render.table)
