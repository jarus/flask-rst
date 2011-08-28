# -*- coding: utf-8 -*-
"""
    flask-rst.modules.staticfiles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os

from flask import current_app, render_template
from flaskrst.parsers import rstDocument
from flaskrst.modules import Blueprint

static_pages = Blueprint('static_pages', __name__, \
                         template_folder='templates')

@static_pages.route('/', defaults={'file_name': 'index'})
@static_pages.route('/<file_name>')
def show(file_name):
    rst_file = os.path.join(current_app.config['SOURCE'], file_name + '.rst')
    rst = rstDocument(rst_file)
    return render_template("static_page.html", page=rst)
    
def setup(app, cfg):
    app.register_blueprint(static_pages)