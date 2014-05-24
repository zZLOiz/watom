#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Thomas Chiroux
# Copyright 2014 Artyom Yamshanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>
#
"""common tools for the project
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux',
    'Artyom Yamshanov', ]


import os
import difflib


def read_file(filename):
    try:
        return open(filename, 'r', encoding='utf-8').read().splitlines()
    except IOError:
        return None

def write_file(filename, lines):
    file = open(filename, 'w', encoding='utf-8')
    file.writelines([x + '\n' for x in lines])
    file.close()

def get_clean_diff(orig, new):
    return [x for x in difflib.Differ().compare(orig, new) if not x.startswith('? ')]


def merge_files(their, orig, own):
    diff_their = get_clean_diff(orig, their)
    diff_own = get_clean_diff(orig, own)

    m = []
    index_their = 0
    index_own = 0
    had_conflict = 0

    while (index_their < len(diff_their)) and (index_own < len(diff_own)):
        # no changes or adds on both sides
        if (diff_their[index_their] == diff_own[index_own] and
                (diff_their[index_their].startswith('  ') or diff_their[index_their].startswith('+ '))):
            m.append(diff_their[index_their][2:])
            index_their += 1
            index_own += 1
            continue

        # removing matching lines from one or both sides
        if ((diff_their[index_their][2:] == diff_own[index_own][2:])
            and (diff_their[index_their].startswith('- ') or diff_own[index_own].startswith('- '))):
            index_their += 1
            index_own += 1
            continue

        # adding lines in A
        if diff_their[index_their].startswith('+ ') and diff_own[index_own].startswith('  '):
            m.append(diff_their[index_their][2:])
            index_their += 1
            continue

        # adding line in B
        if diff_own[index_own].startswith('+ ') and diff_their[index_their].startswith('  '):
            m.append(diff_own[index_own][2:])
            index_own += 1
            continue

        # conflict - list both A and B, similar to GNU's diff3
        m.append("<<<<<<< THEIR")
        while (index_their < len(diff_their)) and not diff_their[index_their].startswith('  '):
            m.append(diff_their[index_their][2:])
            index_their += 1
        m.append("=======")
        while (index_own < len(diff_own)) and not diff_own[index_own].startswith('  '):
            m.append(diff_own[index_own][2:])
            index_own += 1
        m.append(">>>>>>> OWN")
        had_conflict = 1

    # append remining lines - there will be only either A or B
    for i in range(len(diff_their) - index_their):
        m.append(diff_their[index_their + i][2:])
    for i in range(len(diff_own) - index_own):
        m.append(diff_own[index_own + i][2:])

    return had_conflict, m


def watom_distro_path():
    """return the absolute complete path where watom is located

    .. todo:: use pkg_resources ?
    """
    return os.path.dirname(os.path.abspath(__file__))
