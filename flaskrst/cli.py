# -*- coding: utf-8 -*-
"""
    flask-rst.cli
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os

from flaskext.script import Manager
from flaskrst import app, set_source

def create_app(source):
    set_source(app, source)
    return app

manager = Manager(create_app)
manager.add_option("-s", "--source", dest="source", required=False, \
                   default=os.getcwd())
@manager.command
@manager.option('-b', '--build', dest="build_destination", required=False)
def build(build_destination=None):
    """Create a static version of the site with Frozen-Flask"""
    try:
        from flaskext.frozen import Freezer
    except ImportError:
        import sys
        sys.exit("To create a static version of the site you need the "
                 "Frozen-Flask package")

    if build_destination is not None:
        app.config['FREEZER_DESTINATION'] = build_destination
    else:
        app.config['FREEZER_DESTINATION'] = os.path.join(
        app.config["SOURCE"], "_build")

    freezer = Freezer(app)
    freezer.freeze()

def main():
    manager.run()