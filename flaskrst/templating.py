# -*- coding: utf-8 -*-
"""
    flask-rstblog
    ~~~~~~~~~~~~~

    :copyright: (c) 2012 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import current_app, url_for

def inject_navigation():
    navigation = []
    for item in current_app.config.get('NAVIGATION', []):
        if item.has_key('route') and item.has_key('label'):
            kwargs = item.copy()
            del kwargs['route']
            del kwargs['label']

            link = url_for(item['route'], **kwargs)
            navigation.append((link, item['label']))
        elif item.has_key('url') and item.has_key('label'):
            navigation.append((item['url'], item['label']))

    return dict(navigation=navigation)

def _inject_default_stylesheet():
    if len(current_app.config['STYLESHEETS']) == 0:
        url = url_for('static', filename='style.css')
        current_app.config['STYLESHEETS'].append(url)

def inject_default_stylesheet(app):
    if hasattr(app, 'before_first_request'):
        app.before_first_request(_inject_default_stylesheet)
    else:
        app.before_request(_inject_default_stylesheet)
    
    