# -*- coding: utf-8 -*-
"""
    flask-rst.parsers
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
import yaml

from flask import abort
from jinja2 import Markup
from docutils.core import publish_parts

class rstDocument(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path).split(".")[0]
        self._config = None
        self._rst = None
        if not os.path.isfile(self.file_path):
            abort(404)
        with open(self.file_path) as f:
            file_content = f.read()
            self._config, self._rst = file_content.split("\n\n", 1)
    
    @property
    def config(self):
        if not isinstance(self._config, dict):
            self._config = yaml.load(self._config)
            self._config.setdefault('public', False)
        return self._config    

    @property
    def rst(self):
        if not isinstance(self._rst, dict):
            self._rst = publish_parts(source=self._rst, \
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