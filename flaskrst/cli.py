# -*- coding: utf-8 -*-
"""
    flask-rst.cli
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flaskext.script import Manager
from flaskrst import app

def create_app():
    return app

def main():
    manager = Manager(create_app)
    manager.run()