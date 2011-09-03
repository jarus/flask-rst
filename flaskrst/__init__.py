# -*- coding: utf-8 -*-
"""
    flask-rstblog
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, url_for, g

app = Flask("flaskrst")

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