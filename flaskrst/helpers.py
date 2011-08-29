# -*- coding: utf-8 -*-
"""
    flask-rst.helpers
    ~~~~~~~~~~~~~~~~~
    
    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from math import ceil

class Pagination(object):

    def __init__(self, items, page, per_page=10):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total_count = len(items)

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def page_content(self):
        start = self.page * self.per_page - self.per_page
        stop = start + self.per_page
        return self.items[start:stop]