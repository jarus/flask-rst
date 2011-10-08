# -*- coding: utf-8 -*-
"""
    flask-rst.modules.atom
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, current_app
from werkzeug.contrib.atom import AtomFeed, FeedEntry

from flaskrst.modules.blog import get_posts

atom = Blueprint('atom', __name__)

@atom.route("/atom.xml")
def atom_feed():
    feed = AtomFeed(current_app.config.get('SITE_NAME', "My Site"), 
                    feed_url=request.url, url=request.host_url,
                    subtitle=current_app.config.get('SITE_SUBTITLE', None))
    for post in get_posts():
        entry = FeedEntry(post.title, 
                          url=post.external_url,
                          updated=post.pub_date, 
                          content=post.body,
                          summary=post.config.get('summary', None), 
                          author={
                            'name': current_app.config.get('AUTHOR_NAME'),
                            'email': current_app.config.get('AUTHOR_EMAIL')
                          })
        feed.add(entry)
    return feed.to_string(), 200, {}, "application/atom+xml"
    
def setup(app, cfg):
    app.register_blueprint(atom)