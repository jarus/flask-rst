# -*- coding: utf-8 -*-
"""
    flask-rst.cli
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
import yaml

from flaskext.script import Manager
from flaskrst import app
from flaskrst.modules import load_modules

def load_yaml_config(app):
    cfg_path = os.path.join(app.config["SOURCE"], 'config.yml')
    if os.path.isfile(cfg_path):
        cfg = open(cfg_path).read()
        cfg = yaml.load(cfg)
        app.config.update(cfg)
    cfg_static_folder = os.path.join(app.config["SOURCE"], "_static")
    if os.path.isdir(cfg_static_folder):
        app.static_folder = cfg_static_folder
    
def create_app(source):
    app.config["SOURCE"] = source
    load_yaml_config(app)
    load_modules(app)
    return app

def main():
    manager = Manager(create_app)
    manager.add_option("-s", "--source", dest="source", required=False, \
                       default=os.getcwd())
    manager.run()