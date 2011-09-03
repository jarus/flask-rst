# -*- coding: utf-8 -*-
"""
    flask-rstblog
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, url_for

app = Flask("flaskrst")

@app.context_processor
def inject_navigation():
    navigation = []
    for item in app.config.get('NAVIGATION', []):
        kwargs = item.copy()
        del kwargs['route']
        del kwargs['name']
        
        link = url_for(item['route'], **kwargs)
        navigation.append((link, item['name']))
        
    return dict(navigation=navigation)