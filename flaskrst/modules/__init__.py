# -*- coding: utf-8 -*-
"""
    flask-rst.modules
    ~~~~~~~~~~~~~~~~~

    Module interface inspired by Armin Ronacher rstblog. 

    :copyright: (c) 2011 by Christoph Heer
    :license: BSD, see LICENSE for more details.
"""

import sys
import os

from jinja2 import FileSystemLoader
from flask import Blueprint, current_app

def find_module(name):
    full_name = 'flaskrst.modules.' + name
    __import__(full_name)
    return sys.modules[full_name]
    
def load_modules(app):
    for module, cfg in app.config['MODULES'].items():
        if not cfg['active']: continue
        module = find_module(module)
        module.setup(app, cfg)
        
class Blueprint(Blueprint):
    @property
    def jinja_loader(self):
        return FileSystemLoader([
            os.path.join(os.path.dirname(__file__), "..", "templates"),
            os.path.join(self.root_path, self.template_folder),
        ])