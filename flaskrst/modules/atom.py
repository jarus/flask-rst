# -*- coding: utf-8 -*-
"""
    flask-rst.modules.atom
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, current_app, url_for, make_response
from werkzeug.contrib.atom import AtomFeed, FeedEntry

from flaskrst.modules.blog import posts
from .tags import get_posts_by_tag

atom = Blueprint('atom', __name__)

def _generate_entry(post):
    return FeedEntry(post.title,
                     url=post.external_url,
                     updated=post.pub_date,
                     content=post.body,
                     summary=post.config.get('summary', None),
                     author={
            'name': current_app.config.get('AUTHOR_NAME'),
            'email': current_app.config.get('AUTHOR_EMAIL')
            })

@atom.route("/feed.atom")
def atom_feed():
    feed = AtomFeed(current_app.config.get('SITE_NAME', "My Site"),
                    feed_url=request.url, url=request.host_url,
                    subtitle=current_app.config.get('SITE_SUBTITLE', None))
    for post in posts:
        entry = _generate_entry(post)
        feed.add(entry)
    resp = make_response(feed.to_string())
    resp.mimetype = "application/atom+xml"
    return resp

@atom.route("/feed/tag/<tag>.atom")
def atom_feed_tag(tag):
    feed = AtomFeed("%s [%s]" % (current_app.config.get('SITE_NAME', "My Site"),
                                 tag),
                    feed_url=request.url, url=request.host_url,
                    subtitle="%s [%s]" % (
            current_app.config.get('SITE_SUBTITLE', None), tag))
    for post in get_posts_by_tag(tag):
        entry = _generate_entry(post)
        feed.add(entry)
    resp = make_response(feed.to_string())
    resp.mimetype = "application/atom+xml"
    return resp

def setup(app, cfg):
    app.register_blueprint(atom)

    @app.before_request
    def inject_atom_feed():
        atom_feed = (url_for('atom.atom_feed'), 'application/atom+xml',
                     app.config.get("SITE_NAME") + " Atom Feed")
        if app.config['FEEDS'].count(atom_feed) < 1:
            app.config['FEEDS'].append(atom_feed)
