# -*- coding: utf-8 -*-
"""
    flask-rst.modules.blog
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
import re
from datetime import date

from flask import Blueprint, render_template, current_app, url_for

from flaskrst.helpers import Pagination
from flaskrst.parsers import rstDocument

blog_posts_path_re = re.compile(r".*?/(\d{4})/(\d{1,2})/(\d{1,2})/([A-Za-z0-9-]+).rst$")

class BlogPost(rstDocument):
    
    def __init__(self, rst_file):
        super(BlogPost, self).__init__(rst_file)
        
        match = blog_posts_path_re.match(self.file_path)
        self.year = int(match.group(1))
        self.month = int(match.group(2))
        self.day = int(match.group(3))
        self.pub_date = date(self.year, self.month, self.day)
        
        self.link = url_for('blog.post', year=self.year, month=self.month, \
                            day=self.day, file_name=self.file_name)
    
    def __repr__(self):
        return "<BlogPost %s %s>" % (self.file_name, \
                                     self.pub_date.strftime("%Y-%m-%d"))


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

blog = Blueprint('blog', __name__)

@blog.route("/", defaults={'page': 1})
@blog.route("/page/<int:page>/")
def index(page):
    posts = get_posts()
    return render_template('blog_index.html', 
        posts=Pagination(posts, page)
    )

@blog.route("/<int:year>/<int:month>/<int:day>/<file_name>/")
def post(year, month, day, file_name):
    rst_file = os.path.join(current_app.config['SOURCE'], str(year), \
                            str(month), str(day), file_name + ".rst")
    post = BlogPost(rst_file)
    return render_template('blog_post.html',
        post=post
    )
    
def setup(app, cfg):
    app.register_blueprint(blog)
    