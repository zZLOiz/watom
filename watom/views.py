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
"""bottle views for watom
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux',
    'Artyom Yamshanov', ]

import os
import glob
import re
import datetime
import difflib
import urllib
import json

# dependencies imports
from enum import Enum
from bottle import request, response, template, abort, redirect, static_file
import docutils
from docutils.core import publish_parts, publish_doctree
from docutils.writers.html4css1 import Writer as HisWriter
from docutils import io, nodes


# project imports
from watom.rst_directives import todo, done
import watom.tools as tools


def normalize_path(name):
    if not name:
        name = ""
    path_chains = re.split('/|\.', name)

    if not path_chains[-1]:
        if os.path.exists(name + "index.rst"):
            path_chains[-1] = 'index'
        else:
            path_chains[-1] = '__index__'

    return path_chains


def get_id(path_chains):
    return urllib.parse.quote('/' + '/'.join(path_chains))


def get_metaname(path_chains):
    if path_chains[-1] == 'index':
        return (('/' + '/'.join(path_chains[:-1])) if len(path_chains) > 1 else '') + '/__index__'


def get_default_view(name):
    return name[-1] + "\n" + "=" * len(name[-1])

def get_filename(path_chains):
    return '/'.join(path_chains) + '.rst' if path_chains[-1] else ''


def get_breadcrumbs(name):
    current = "/"
    crumbs = []
    for e in name[:-1]:
        current += e + '/'
        crumbs.append((e, current))

    current += name[-1]
    crumbs.append((name[-1], current))

    return crumbs


def view_meta_cheat_sheet():
    """Display a cheat sheet of reST syntax
    """
    response.set_header('Content-Type', 'text/plain')
    return template('rst_cheat_sheet')


def view_meta_index(name):
    """List all the available .rst files in the directory

    view_meta_index is called by the 'meta' url : /__index__'./' + dir_path + pathos.path.isfile('./' + dir_path + path)
    """
    dirs = []
    files = []
    dir_path = '/'.join(name[:-1]) + '/'

    if os.path.exists('./' + dir_path):
        for path in os.listdir('./' + dir_path):
            if os.path.isfile('./' + dir_path + path) and path[-4:] == '.rst':
                files.append(path[:-4])
            elif os.path.isdir('./' + dir_path + path):
                files.append(path + '/')

    return template('index',
                    type="view",
                    filelist=files,
                    name=get_id(name),
                    breadcrumbs=get_breadcrumbs(name))


def view_meta_admonition(admonition_name, name=None):
    """List all found admonition from all the rst files found in directory

    view_meta_admonition is called by the 'meta' url: /__XXXXXXX__
    where XXXXXXX represents and admonition name, like:

    * todo
    * warning
    * danger
    * ...

    .. note:: this function may works for any docutils node, not only
       admonition

    Keyword Arguments:

        :admonition_name: (str) -- name of the admonition
    """
    print(("meta admo: %s - %s" % (admonition_name, name)))
    admonition = None

    if admonition_name == 'todo':
        admonition = todo
    elif admonition_name == 'done':
        admonition = done
    elif hasattr(nodes, admonition_name):
        admonition = getattr(nodes, admonition_name)
    else:
        return abort(404)

    doc2_content = ""

    doc2_output, doc2_pub = docutils.core.publish_programmatically(
        source_class=io.StringInput,
        source=doc2_content,
        source_path=None,
        destination_class=io.StringOutput,
        destination=None, destination_path=None,
        reader=None, reader_name='standalone',
        parser=None, parser_name='restructuredtext',
        writer=HisWriter(), writer_name=None,
        settings=None, settings_spec=None,
        settings_overrides=None,
        config_section=None,
        enable_exit_status=False)

    section1 = nodes.section("{0}_list_file".format(admonition_name))
    doc2_pub.reader.document.append(section1)
    title1 = nodes.title("{0} LIST".format(admonition_name.upper()),
                         "{0} LIST".format(admonition_name.upper()))
    doc2_pub.reader.document.append(title1)
    if name is None:
        rst_files = [filename[2:-4] for filename in sorted(
            glob.glob("./*.rst"))]
        rst_files.reverse()
    else:
        rst_files = [filename[2:-4] for filename in
                     sorted(glob.glob("./{0}.rst".format(name)))]
    for file in rst_files:
        file_title = False
        file_handle = open(file + '.rst', 'r', encoding='utf-8')
        file_content = file_handle.read()
        file_handle.close()
        file_content = file_content

        output, pub = docutils.core.publish_programmatically(
            source_class=io.StringInput, source=file_content,
            source_path=None,
            destination_class=io.StringOutput,
            destination=None, destination_path=None,
            reader=None, reader_name='standalone',
            parser=None, parser_name='restructuredtext',
            writer=None, writer_name='html',
            settings=None, settings_spec=None,
            settings_overrides=None,
            config_section=None,
            enable_exit_status=False)

        my_settings = pub.get_settings()
        parser = docutils.parsers.rst.Parser()
        document = docutils.utils.new_document('test', my_settings)
        parser.parse(file_content, document)
        for node in document.traverse(admonition):
            if not file_title:
                file_title = True
                # new section
                section2 = nodes.section(file)
                doc2_pub.reader.document.append(section2)
                # add link to the originating file
                paragraph = nodes.paragraph()
                file_target = nodes.target(ids=[file],
                                           names=[file],
                                           refuri="/" + file)
                file_ref = nodes.reference(file, file,
                                           name=file,
                                           refuri="/" + file)
                paragraph.append(nodes.Text("in "))
                paragraph.append(file_ref)
                paragraph.append(file_target)
                paragraph.append(nodes.Text(":"))
                doc2_pub.reader.document.append(paragraph)
                #doc2_pub.reader.document.append(file_target)

            doc2_pub.reader.document.append(node)
        doc2_pub.apply_transforms()

    doc2_pub.writer.write(doc2_pub.document, doc2_pub.destination)
    doc2_pub.writer.assemble_parts()
    if name is None:
        display_file_name = '__{0}__'.format(admonition_name)
        extended_name = None
    else:
        display_file_name = '{0}'.format(name)
        extended_name = '__{0}__'.format(admonition_name)
    return template('page',
                    type="view",
                    name=display_file_name,
                    content=doc2_pub.writer.parts['html_body'])


def view_edit(name=None):
    """edit or creates a new page

    .. note:: this is a bottle view

    if no page name is given, creates a new page.

    Keyword Arguments:
        :name: (str) -- name of the page (OPTIONAL)

    Returns:
        bottle response object
    """
    response.set_header('Cache-control', 'no-cache')
    response.set_header('Pragma', 'no-cache')

    filename = get_filename(name)

    if os.path.exists(filename):
        file_handle = open(filename, 'r', encoding='utf-8')
        content = file_handle.read()
    else:
        content = get_default_view(name)

    return template('edit',
                    type="edit",
                    name=get_id(name),
                    breadcrumbs=get_breadcrumbs(name),
                    content=content)


def view_preview(name=None):
    """serve a page name

    .. note:: this is a bottle view

    * if the view is called with the POST method, write the new page
      content to the file, commit the modification and then display the
      html rendering of the restructured text file

    * if the view is called with the GET method, directly display the html
      rendering of the restructured text file

    Keyword Arguments:
        :name: (str) -- name of the rest file (without the .rst extension)
                        OPTIONAL

    if no filename is given, first try to find a "index.rst" file in the
    directory and serve it. If not found, serve the meta page __index__

    Returns:
        bottle response object
    """

    response.set_header('Cache-control', 'no-cache')
    response.set_header('Pragma', 'no-cache')

    filename = get_filename(name)
    html_body = ""
    if os.path.exists(filename):
        file_handle = open(filename, 'r', encoding='utf-8')
        html_body = publish_parts(file_handle.read(),
                                  writer=HisWriter(),
                                  settings=None,
                                  settings_overrides=None)['html_body']

    return template('preview',
                    type="view",
                    name=get_id(name),
                    extended_name=None,
                    content=html_body)


def view_page(name):
    filename = get_filename(name)
    if os.path.exists(filename):
        file_handle = open(filename, 'r', encoding='utf-8')
        html_body = publish_parts(file_handle.read(),
                                  writer=HisWriter(),
                                  settings=None,
                                  settings_overrides=None)['html_body']

        return template('page',
                        type="view",
                        name=get_id(name),
                        meta=get_metaname(name),
                        breadcrumbs=get_breadcrumbs(name),
                        content=html_body)
    else:
        return redirect(get_id(name) + ".__edit__")


def view_resource(name):
    return static_file(name, os.path.join(tools.watom_distro_path(), 'res'))


def page_router(name=None):
    """serve a page name

    .. note:: this is a bottle view

    * if the view is called with the POST method, write the new page
      content to the file, commit the modification and then display the
      html rendering of the restructured text file

    * if the view is called with the GET method, directly display the html
      rendering of the restructured text file

    Keyword Arguments:
        :name: (str) -- name of the rest file (without the .rst extension)
                        OPTIONAL

    if no filename is given, first try to find a "index.rst" file in the
    directory and serve it. If not found, serve the meta page __index__

    Returns:
        bottle response object
    """

    response.set_header('Cache-control', 'no-cache')
    response.set_header('Pragma', 'no-cache')

    if name is not None and os.path.exists(name) and os.path.isfile(name):
        return static_file(name, '')

    name = normalize_path(name)

    if name[-1] == "__index__":
        return view_meta_index(name)
    elif name[-1] == "__edit__":
        return view_edit(name[:-1])
    elif name[-1] == "__preview__":
        return view_preview(name[:-1])
    else:
        return view_page(name)


def save_page(name=None):
    """quick save a page

    .. note:: this is a bottle view

    * this view must be called with the PUT method
      write the new page content to the file, and not not commit or redirect

    Keyword Arguments:
        :name: (str) -- name of the rest file (without the .rst extension)

    Returns:
        bottle response object (200 OK)
    """
    response.set_header('Cache-control', 'no-cache')
    response.set_header('Pragma', 'no-cache')
    if request.method == 'PUT' or request.method == 'POST':
        name = normalize_path(name)
        file_name = get_filename(name[:-1])
        dir_name = os.path.dirname(file_name)
        if len(dir_name) > 0 and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        if name is not None:
            if request.method == 'PUT':
                input_data = json.loads(request.body.read().decode('utf-8'))
                new_content = input_data['new_content']
                old_content = input_data['old_content']
            else:
                new_content = request.forms.getunicode('new_content')
                old_content = request.forms.getunicode('old_content')

            new_content = new_content.splitlines()
            old_content = old_content.splitlines()
            file_content = tools.read_file(file_name)

            if file_content:
                has_conflict, merged_content = tools.merge_files(file_content, old_content, new_content)
            else:
                has_conflict, merged_content = False, new_content

            tools.write_file(file_name, merged_content)

            if request.method == 'PUT':
                return json.dumps(dict(
                    result="OK" if not has_conflict else "CONFLICTED",
                    updated_content='\n'.join(merged_content)
                ))
            else:
                redirect(get_id(name[:-1]) + ('' if not has_conflict else '.__edit__'))
        else:
            return abort(404)
