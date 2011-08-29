# -*- coding: utf-8 -*-
"""
    flask-rst.modules.blog.parsers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import re
from datetime import date

from flask import url_for
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
