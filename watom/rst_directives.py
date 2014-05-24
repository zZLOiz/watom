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
"""adds restructured text directives to docutils
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux',
    'Artyom Yamshanov', ]

from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils import nodes, utils
from docutils.parsers.rst import directives

YOUTUBE_CODE = """\
<div><object type="application/x-shockwave-flash"
        width="%(width)s"
        height="%(height)s"
        class="youtube-embed"
        data="http://www.youtube.com/v/%(yid)s">
    <param name="movie" value="http://www.youtube.com/v/%(yid)s"></param>
    <param name="wmode" value="transparent"></param>%(extra)s
</object></div>
"""

YOUTUBE_PARAM = """\n    <param name="%s" value="%s"></param>"""

MATHJAX_SCRIPT = """\
<script type="text/javascript" 
   src="/__res__/mathjax/MathJax.js?config=TeX-AMS-MML_SVG-full">
</script>
<script type="text/x-mathjax-config"> 
   MathJax.Hub.Config({showMathMenu: false}); 
</script> 
"""

MATHJAX_BLOCK = "\\[%s\\]"

MATHJAX_INLINE = "\\(%s\\)"

def add_node(node, **kwds):
    """add_node from Sphinx
    """
    nodes._add_node_class_names([node.__name__])
    for key, val in list(kwds.items()):
        try:
            visit, depart = val
        except ValueError:
            raise ValueError('Value for key %r must be a '
                                 '(visit, depart) function tuple' % key)
        if key == 'html':
            from docutils.writers.html4css1 import HTMLTranslator as translator
        elif key == 'latex':
            from docutils.writers.latex2e import LaTeXTranslator as translator
        else:
            # ignore invalid keys for compatibility
            continue
        setattr(translator, 'visit_'+node.__name__, visit)
        if depart:
            setattr(translator, 'depart_'+node.__name__, depart)

class todo(nodes.Admonition, nodes.Element):
    """todo node for docutils"""
    pass


def visit_todo(self, node):
    self.visit_admonition(node)


def depart_todo(self, node):
    self.depart_admonition(node)


class Todo(BaseAdmonition):
    """todo directive for docutils

    uses BaseAdmonition from docutils (like .. note:: of .. warning:: etc..)
    """
    optional_arguments = 0
    node_class = todo


class done(nodes.Admonition, nodes.Element):
    """done node for docutils"""
    pass


def visit_done(self, node):
    self.visit_admonition(node)


def depart_done(self, node):
    self.depart_admonition(node)


class Done(BaseAdmonition):
    """done directive for docutils

    uses BaseAdmonition from docutils (like .. note:: of .. warning:: etc..)
    """
    optional_arguments = 0
    node_class = done

def youtube(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    """ Restructured text extension for inserting youtube embedded videos """
    if len(content) == 0:
        return
    string_vars = {
        'yid': content[0],
        'width': 425,
        'height': 344,
        'extra': ''
        }
    extra_args = content[1:] # Because content[0] is ID
    extra_args = [ea.strip().split("=") for ea in extra_args] # key=value
    extra_args = [ea for ea in extra_args if len(ea) == 2] # drop bad lines
    extra_args = dict(extra_args)
    if 'width' in extra_args:
        string_vars['width'] = extra_args.pop('width')
    if 'height' in extra_args:
        string_vars['height'] = extra_args.pop('height')
    if extra_args:
        params = [YOUTUBE_PARAM % (key, extra_args[key]) for key in extra_args]
        string_vars['extra'] = "".join(params)
    return [nodes.raw('', YOUTUBE_CODE % (string_vars), format='html')]

def latex_math_enable(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    return [nodes.raw('', MATHJAX_SCRIPT, format='html')]

def latex_math(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    if len(content) == 0:
        return
    return [nodes.raw('', MATHJAX_BLOCK % '\n'.join([utils.unescape(x, True) for x in content]), format='html')]

def latex_math_inline(name, rawtext, text, lineno, inliner,
            options={}, content=[]):
    return [nodes.raw('', MATHJAX_INLINE % utils.unescape(text, True), format='html')], []
