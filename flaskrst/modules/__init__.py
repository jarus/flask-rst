# -*- coding: utf-8 -*-
"""
    flask-rst.modules
    ~~~~~~~~~~~~~~~~~

    Module interface inspired by Armin Ronacher rstblog. 

    :copyright: (c) 2011 by Christoph Heer
    :license: BSD, see LICENSE for more details.
"""

import sys

def find_module(name):
    full_name = 'flaskrst.modules.' + name
    __import__(full_name)
    return sys.modules[full_name]
    
def load_modules(app):
    for module, cfg in app.config.get('MODULES', {}).items():
        if not cfg.get('active', False): continue
        module = find_module(module)
        module.setup(app, cfg)