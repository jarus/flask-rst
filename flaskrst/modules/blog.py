# -*- coding: utf-8 -*-
"""
    flask-rst.modules.blog
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
import re
import time
from datetime import date

from flask import Blueprint, render_template, current_app, url_for, abort, request, g
from werkzeug.datastructures import OrderedMultiDict

from flaskrst.helpers import Pagination
from flaskrst.parsers import rstDocument

blog_config = {}
blog_posts_path_re = re.compile(
    r".*?/(\d{4})/(\d{1,2})/(\d{1,2})/([A-Za-z0-9-\_\.]+).rst$"
)

def generate_post_id(year, month, day, file_name):
    return "%04d-%02d-%02d-%s" % (int(year), int(month), int(day), file_name) 

class BlogPost(rstDocument):
    
    def __init__(self, rst_file):
        super(BlogPost, self).__init__(rst_file)
        
        match = blog_posts_path_re.match(self.file_path)
        self.year = int(match.group(1))
        self.month = int(match.group(2))
        self.day = int(match.group(3))
        self.pub_date = date(self.year, self.month, self.day)
        
        self.id = generate_post_id(self.year, self.month, self.day, 
                                   self.file_name)

    @property
    def public(self):
        return self.config.get("public", False)
        
    @property
    def url(self):
        return url_for('blog.post', year=self.year, month=self.month,
                        day=self.day, file_name=self.file_name)
    
    @property
    def external_url(self):
        return url_for('blog.post', year=self.year, month=self.month, 
                       day=self.day, file_name=self.file_name, _external=True)
    
    @property
    def summary(self):
        if 'summary' in self.config:
            return self.config['summary']
        elif blog_config.get('body_as_summary_fallback'):
            return self.body
        else:
            return None
    
    def __repr__(self):
        return "<BlogPost %s %s>" % (self.file_name, \
                                     self.pub_date.strftime("%Y-%m-%d"))


class BlogPostCollector():
    
    _posts = {}

    @property
    def _post_list(self):
        keys = self._posts.keys()
        keys.sort()
        keys.reverse()            
        return [self._posts[key] for key in keys]

    def __init__(self, root_path=None):
        if root_path:
            self.root_path = root_path
            self.fetch()

    def fetch(self):
        if request:
            if hasattr(g, "_blogpostsfetched"):
                return
            else:
                g._blogpostsfetched = True

        for root, dirs, files in os.walk(self.root_path):
            dirs = [_dir for _dir in dirs if not _dir.startswith('_')]
            for f in files:
                file_path = os.path.join(root, f)
                match = blog_posts_path_re.match(file_path)
                if match:
                    post_id = generate_post_id(*match.groups())
                    if post_id not in self._posts:
                        post = BlogPost(file_path)
                        if post.public:
                            self._posts[post.id] = post

    def __len__(self):
        self.fetch()
        return len(self._post_list)

    def __iter__(self):
        self.fetch()
        return self._post_list.__iter__()

    def index(self, post):
        return self._post_list.index(post)

    def __getitem__(self, name):
        if name not in self:
            self.fetch()
        
        if isinstance(name, basestring):
            return self._posts[name]
        elif isinstance(name, (int, slice)):
            return self._post_list[name]
        else:
            raise KeyError("Post by key (%s) not found" % (name))
    
    def __hasitem__(self, name):
        if isinstance(name, basestring):
            if name not in self._posts:
                self.fetch()
            return name in self._posts
        elif isinstance(name, (int, slice)):
            if len(self._post_list) < name:
                self.fetch()
            return len(self._post_list) >= name
        else:
            return False
    
    __contains__ = __hasitem__

    def __repr__(self):
        return "<BlogPostCollector %s>" % self._post_list

posts = BlogPostCollector()
blog = Blueprint('blog', __name__)

@blog.route("/", defaults={'page': 1})
@blog.route("/page/<int:page>/")
def index(page):
    return render_template('blog_index.html', 
        posts=Pagination(posts, page)
    )

@blog.route("/<int:year>/<int:month>/<int:day>/<file_name>/")
def post(year, month, day, file_name):    
    post_id = generate_post_id(year, month, day, file_name)

    if post_id not in posts:
        abort(404)
    post = posts[post_id]
    post_index = posts.index(post)

    prev_post = None
    next_post = None
    if post_index > 0:
        prev_post = posts[post_index-1]
    if post_index < len(posts)-1:
        next_post = posts[post_index+1]
        
    return render_template('blog_post.html', post=post,
                           prev=prev_post, next=next_post)
    
def setup(app, cfg):
    global blog_config
    blog_config = cfg
    
    posts.root_path = app.config['SOURCE']
    posts.fetch()
        
    app.register_blueprint(blog)
    
