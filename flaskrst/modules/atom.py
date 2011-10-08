# -*- coding: utf-8 -*-
"""
    flask-rst.modules.atom
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, current_app
from werkzeug.contrib.atom import AtomFeed

atom = Blueprint('atom', __name__)

@atom.route("/atom.xml")
def atom_feed():
    print dir(atom)
    feed = AtomFeed(current_app.config.get('SITE_NAME', "My Site"), 
                    feed_url=request.url, url=request.host_url,
                    subtitle=current_app.config.get('SITE_SUBTITLE', None))
    return feed.to_string(), 200, {}, "application/atom+xml"
    
def setup(app, cfg):
    app.register_blueprint(atom)