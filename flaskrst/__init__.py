# -*- coding: utf-8 -*-
"""
    flask-rstblog
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
from datetime import date

from jinja2 import FileSystemLoader
from flask import Flask, url_for

from flaskrst.modules import load_modules

class Flask(Flask):
    def create_global_jinja_loader(self):
        template_path = os.path.join(self.config.get('SOURCE', ''),
                                     "_templates")
        builtin_templates = os.path.join(self.root_path,
                                         self.template_folder)
        return FileSystemLoader([template_path, builtin_templates])
        
app = Flask("flaskrst")
app.config['STYLESHEETS'] = []
app.jinja_env.globals['date'] = date

def set_source(app, source_path=os.getcwd()):
    app.config['SOURCE'] = source_path
    source_static_folder = os.path.join(source_path, "_static")
    if os.path.isdir(source_static_folder):
        app.static_folder = source_static_folder
    app.config.from_pyfile(os.path.join(app.config['SOURCE'], 'config.py'))
    load_modules(app)

set_source(app)

@app.context_processor
def inject_navigation():
    navigation = []
    for item in app.config.get('NAVIGATION', []):
        if item.has_key('route') and item.has_key('label'):
            kwargs = item.copy()
            del kwargs['route']
            del kwargs['label']
        
            link = url_for(item['route'], **kwargs)
            navigation.append((link, item['label']))
        elif item.has_key('url') and item.has_key('label'):
            navigation.append((item['url'], item['label']))

    return dict(navigation=navigation)

@app.before_request
def inject_stylesheet():
    app.config['STYLESHEETS'].append(url_for('static', filename='style.css'))
