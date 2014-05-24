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
"""get version for the module
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux',
    'Artyom Yamshanov', ]


import pkg_resources

__version__ = "unknown"

try:
    __version__ = pkg_resources.resource_string("watom",
                                                "RELEASE-VERSION").strip()
except IOError:
    __version__ = "0.0.0"
