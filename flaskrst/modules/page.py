# -*- coding: utf-8 -*-
"""
    flask-rst.modules.staticfiles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, current_app, render_template, safe_join
from flaskrst.parsers import rstDocument

page = Blueprint('page', __name__)

@page.route('/', defaults={'file_path': 'index'})
@page.route('/<path:file_path>/')
def show(file_path):
    if file_path.endswith('/'):
        file_path += "index"
    rst_file = safe_join(current_app.config['SOURCE'], file_path + '.rst')
    rst = rstDocument(rst_file)
    return render_template("page_show.html", page=rst)
    
def setup(app, cfg):
    app.register_blueprint(page)