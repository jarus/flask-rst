# -*- coding: utf-8 -*-
"""
    flask-rst.modules.staticfiles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os

from flask import Blueprint, current_app
from flaskrst.parsers import rstDocument

static_pages = Blueprint('static_pages', __name__)

@static_pages.route('/', defaults={'file_name': 'index'})
@static_pages.route('/<file_name>')
def show(file_name):
    rst_file = os.path.join(current_app.config['SOURCE'], file_name + '.rst')
    rst = rstDocument(rst_file)
    return rst.title + rst.body