# -*- coding: utf-8 -*-
"""
    flask-rst.cli
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
import datetime

from flask import current_app

from flask.ext.script import Manager, prompt
from flaskrst import create_app

manager = Manager(create_app)
manager.add_option("-s", "--source", dest="source", required=False, \
                   default=os.getcwd())
@manager.command
@manager.option('-b', '--build', dest="build_destination", required=False)
def build(build_destination=None):
    """Create a static version of the site with Frozen-Flask"""
    try:
        from flask.ext.frozen import Freezer
    except ImportError:
        import sys
        sys.exit("To create a static version of the site you need the "
                 "Frozen-Flask package")

    if build_destination is not None:
        current_app.config['FREEZER_DESTINATION'] = build_destination
    else:
        current_app.config['FREEZER_DESTINATION'] = os.path.join(
        current_app.config["SOURCE"], "_build")

    freezer = Freezer(current_app)
    freezer.freeze()


def _read_date():
    """ read date from input; default to today """
    # show date
    while 1:
        dts = prompt("Date", default=str(datetime.date.today()))
        try:
            datetime.datetime.strptime(dts, "%Y-%m-%d")
            break
        except ValueError:
            continue
    return dts

@manager.command
def new():
    """Create new blog post (including directories)
       and run $EDITOR (fallback to vi)."""
    # read date
    dt = _read_date()
    # make directorie(s)
    path = dt.replace('-','/')
    try: 
        os.makedirs(path)
    except OSError:
        pass
    # chdir to that directory
    os.chdir(path)
    # run $EDITOR, with default to vi (should exist on every unix)
    os.system(os.getenv('EDITOR', 'vi'))
    
def main():
    manager.run()
