# -*- coding: utf-8 -*-
"""
    flask-rst.modules.blog
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os

from flask import Blueprint, render_template, current_app
from flaskrst.helpers import Pagination

from flaskrst.modules.blog.parsers import BlogPost, blog_posts_path_re

def get_posts():
    posts = []
    for root, dirs, files in os.walk(current_app.config['SOURCE']):
        dirs = [_dir for _dir in dirs if not _dir.startswith('_')]
        for f in files:
            file_path = os.path.join(root, f)
            if blog_posts_path_re.match(file_path):
                posts.append(file_path)
    posts.sort()
    posts.reverse()
    posts = [BlogPost(rst_file) for rst_file in posts]
    for blog_post in posts:
        if not blog_post.config.get("public", False):
            posts.remove(blog_post)
    return posts

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route("/", defaults={'page': 1})
@blog.route("/page/<int:page>")
def index(page):
    posts = get_posts()
    return render_template('index.html', 
        posts=Pagination(posts, page)
    )

@blog.route("/<int:year>/<int:month>/<int:day>/<file_name>")
def post(year, month, day, file_name):
    rst_file = os.path.join(current_app.config['SOURCE'], str(year), \
                            str(month), str(day), file_name + ".rst")
    post = BlogPost(rst_file)
    return render_template('post.html',
        post=post
    )
    
def setup(app, cfg):
    app.register_blueprint(blog)
    