# -*- coding: utf-8 -*-
"""
    flask-rst.modules.tags
    ~~~~~~~~~~~~~~~~~~~~~~
    
    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from math import log

from flask import Blueprint, render_template
from jinja2 import Markup
from flaskrst.modules.blog import get_posts

def get_tags():
    tags = {}
    for post in get_posts():
        post_tags = [tag.lower() for tag in post.config.get('tags', [])]
        for tag in post_tags:
            if tag not in tags:
                tags[tag] = 1
            else:
                tags[tag] += 1
    return tags

def get_posts_by_tag(name):
    posts = []
    for post in get_posts():
        post_tags = [tag.lower() for tag in post.config.get('tags', [])]
        for tag in post_tags:
            if tag == name and post not in posts:
                posts.append(post)
    return posts

def template_tags(doc):
    tags = [tag.lower() for tag in doc.config.get('tags', [])]
    return Markup(render_template('tags_inside_post.html', tags=tags))

tags = Blueprint('tags', __name__)

@tags.route("/tags/")
def cloud():
    tags = get_tags()
    for tag in tags:
        tags[tag] = 100 + log(tags[tag] or 1) * 20
    return render_template('tags_cloud.html',
        tags=tags
    )
    
@tags.route("/tags/<tag>/")
def tag(tag):
    blog_posts = get_posts_by_tag(tag)
    return render_template('tags_taged_with.html',
        tag=tag,
        blog_posts=blog_posts
    )

def setup(app, cfg):
    app.jinja_env.globals['tags'] = template_tags
    app.register_blueprint(tags)