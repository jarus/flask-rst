# -*- coding: utf-8 -*-
"""
    flask-rstblog
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask
from flaskrst import modules

app = Flask("flask-rst")
app.register_blueprint(modules.find_module("staticpages").static_pages)