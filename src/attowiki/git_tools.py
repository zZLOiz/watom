#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Thomas Chiroux
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
"""git tools functions used in the project
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]


from git import Repo, InvalidGitRepositoryError


def check_repo():
    """checks is local git repo is present or not

    Keywords Arguments:
        <none>

    Returns:
        boolean -- True if git repo is present, False if not
    """
    try:
        Repo()
    except InvalidGitRepositoryError:
        return False
    return True


def commit(filename):
    """Commit (git) a specified file

    This method does the same than a ::

        $ git commit -a "message"

    Keyword Arguments:
        :filename: (str) -- name of the file to commit

    Returns:
        <nothing>
    """
    try:
        repo = Repo()
        #gitcmd = repo.git
        #gitcmd.commit(filename)
        index = repo.index
        index.commit("Updated file: {0}".format(filename))
    except Exception:
        pass


def add_file_to_repo(filename):
    """Add a file to the git repo

    This method does the same than a ::

        $ git add filename

    Keyword Arguments:
        :filename: (str) -- name of the file to commit

    Returns:
        <nothing>
    """
    try:
        repo = Repo()
        index = repo.index
        index.add([filename])
    except Exception:
        pass


def reset_to_last_commit():
    """reset a modified file to his last commit status

    This method does the same than a ::

        $ git reset --hard

    Keyword Arguments:
        <none>

    Returns:
        <nothing>
    """
    try:
        repo = Repo()
        gitcmd = repo.git
        gitcmd.reset(hard=True)
    except Exception:
        pass