# -*- coding: utf-8 -*-
"""
    flask-rst.cli
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os

from flaskext.script import Manager
from flaskrst import app

def create_app(source):
    app.config["SOURCE"] = source
    print app.config["SOURCE"]
    return app

def main():
    manager = Manager(create_app)
    manager.add_option("-s", "--source", dest="source", required=False, \
                       default=os.getcwd())
    manager.run()