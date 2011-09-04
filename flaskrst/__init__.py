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
from flask import Flask, url_for, g

class Flask(Flask):
    def create_global_jinja_loader(self):
        template_path = os.path.join(self.config.get('SOURCE', ''),
                                     "_templates")
        builtin_templates = os.path.join(self.root_path,
                                         self.template_folder)
        return FileSystemLoader([template_path, builtin_templates])
        
app = Flask("flaskrst")
app.jinja_env.globals['date'] = date

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
    g.stylesheets = [url_for('static', filename='style.css')]