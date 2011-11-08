# -*- coding: utf-8 -*-
"""
    flask-rst.parsers
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import with_statement

import os
import re

from flask import abort
from jinja2 import Markup
from docutils.core import publish_parts

config_parser_re = re.compile(r"^:(\w+): ?(.*?)$", re.M)

class rstDocument(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = ".".join(os.path.basename(self.file_path).split(".")[:-1])
        self._config = None
        self._rst = None
        if not os.path.isfile(self.file_path):
            abort(404)
        with open(self.file_path) as f:
            self.raw = f.read()
    
    @property
    def config(self):
        if not isinstance(self._config, dict):
            self._config = {}
            for m in config_parser_re.finditer(self.raw):
                self._config[m.group(1)] = eval(m.group(2))
            self._config.setdefault('public', False)
        return self._config

    @property
    def rst(self):
        if not isinstance(self._rst, dict):
            self._rst = publish_parts(source=self.raw, \
                                      writer_name='html4css1')
        return self._rst

    @property
    def title(self):
        return Markup(self.rst['title']).striptags()

    @property
    def body(self):
        return Markup(self.rst['fragment'])

    def __repr__(self):
        return "<rstDocument %s>" % (self.file_name)
