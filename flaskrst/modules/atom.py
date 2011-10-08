# -*- coding: utf-8 -*-
"""
    flask-rst.modules.atom
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, current_app, url_for
from werkzeug.contrib.atom import AtomFeed, FeedEntry

from flaskrst.modules.blog import get_posts

atom = Blueprint('atom', __name__)

@atom.route("/feed.atom")
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

    @app.before_request
    def inject_atom_feed():
        atom_feed = (url_for('atom.atom_feed'), 'application/atom+xml',
                     app.config.get("SITE_NAME") + " Atom Feed")
        if app.config['FEEDS'].count(atom_feed) < 1:
            app.config['FEEDS'].append(atom_feed)