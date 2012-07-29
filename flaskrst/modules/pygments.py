# -*- coding: utf-8 -*-
"""
    flaskrst.modules.pygments
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import
from docutils import nodes
from docutils.parsers.rst import directives, Directive

from hashlib import sha1
from flask import url_for, make_response, request, abort

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, TextLexer
    from pygments.formatters import HtmlFormatter
except ImportError:
    import sys
    sys.exit("To use pygments in flask-rst you must install pygments")

formatter = HtmlFormatter()

class Pygments(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            lexer = TextLexer()
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

def setup(app, cfg):
    global formatter
    formatter = HtmlFormatter(style=cfg.get('style', 'tango'))
    directives.register_directive('sourcecode', Pygments)
    directives.register_directive('code-block', Pygments)
    
    @app.route(cfg.get('css_file_route', "/static/pygments.css"))
    def pygments_css():
        etag = sha1(str(formatter.style)).hexdigest()
        if request.headers.get('If-None-Match') == etag:
            return "", 304
        else:
            res = make_response(formatter.get_style_defs())
            res.mimetype = "text/css"
            res.headers['ETag'] = etag
            return res
    
    @app.before_request
    def inject_pygments_css():
        if url_for('pygments_css') not in app.config['STYLESHEETS']:
            app.config['STYLESHEETS'].append(url_for('pygments_css'))