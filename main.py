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
"""file for main entry point
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux',
    'Artyom Yamshanov', ]

# dependencies imports
import bottle
import os

from docutils.parsers.rst import directives, roles
from docutils import nodes, languages

# project imports
from watom import views
import watom.rst_directives as watom_rst
from watom.tools import watom_distro_path


# register specific rst directives
# small trick here: get_language will reveal languages.en
labels = languages.get_language('en').labels

# add the label
languages.en.labels["todo"] = "Todo"
# add node
watom_rst.add_node(watom_rst.todo,
         html= (watom_rst.visit_todo, watom_rst.depart_todo),
         latex=(watom_rst.visit_todo, watom_rst.depart_todo),
         text= (watom_rst.visit_todo, watom_rst.depart_todo))
# register the new directive todo
directives.register_directive('todo', watom_rst.Todo)

# add the label
languages.en.labels["done"] = "Done"
# add node
watom_rst.add_node(watom_rst.done,
         html= (watom_rst.visit_done, watom_rst.depart_done),
         latex=(watom_rst.visit_done, watom_rst.depart_done),
         text= (watom_rst.visit_done, watom_rst.depart_done))
# register the new directive done
directives.register_directive('done', watom_rst.Done)

# register the new directive youtube
watom_rst.youtube.content = True
directives.register_directive('youtube', watom_rst.youtube)
directives.register_directive('latex_math_enable', watom_rst.latex_math_enable)
watom_rst.latex_math.content = True
directives.register_directive('latex_math', watom_rst.latex_math)
roles.register_canonical_role('latex_math', watom_rst.latex_math_inline)

# add view path from module localisation
views_path = os.path.join(watom_distro_path(), 'views')
bottle.TEMPLATE_PATH.insert(0, views_path)

app = bottle.Bottle()

# All the Urls of the project
# index or __index__

app.route('/__res__/<name:path>')(views.view_resource)

# view an existing page
app.route('/<name:path>', method='GET')(views.page_router)
app.route('/', method='GET')(views.page_router)

# write new content to an existing page
app.route('/<name:path>', method='POST')(views.save_page)
# write new content to an existing page (without commit - for quick save)
app.route('/<name:path>', method='PUT')(views.save_page)

app.route('/__cheatsheet__')(views.view_meta_cheat_sheet)
app.route('/__<admonition_name>__')(views.view_meta_admonition)
app.route('/<name>.__<admonition_name>__')(views.view_meta_admonition)

# for devt purpose: set bottle in debug mode
bottle.debug(True)  # this line may be commented in production mode

# run locally by default
from optparse import OptionParser
cmd_parser = OptionParser(usage="usage: %prog package.module:app")
cmd_options, cmd_args = cmd_parser.parse_args()
if len(cmd_args) >= 2:
    host, port = (cmd_args[0] or 'localhost'), (cmd_args[1] or 8080)
elif len(cmd_args) == 1:
    host, port = (cmd_args[0] or 'localhost'), (8080)
else:
    host, port = ('localhost'), (8080)
    if ':' in host:
        host, port = host.rsplit(':', 1)

bottle.run(app, host=host, port=port)
