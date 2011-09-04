# -*- coding: utf-8 -*-
"""
    flask-rst.modules.archive
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, render_template, abort
from flaskrst.modules.blog import get_posts

def get_archive():
    archive = {}
    for post in get_posts():
        if not archive.has_key(post.pub_date.year):
            archive[post.pub_date.year] = {}
        if not archive[post.pub_date.year].has_key(post.month):
            archive[post.year][post.month] = []
        archive[post.year][post.month].append(post)
    return archive

archive = Blueprint('archive', __name__)

@archive.route("/archive/")
def index():
    archive = get_archive()
    return render_template('archive_index.html', 
        archive=archive
    )

@archive.route("/<int:year>/")
def year(year):
    archive = get_archive()
    if not archive.has_key(year):
        abort(404)
    return render_template('archive_year.html', 
        archive=archive[year],
        year=year
    )

@archive.route("/<int:year>/<int:month>/")
def month(year, month):
    archive = get_archive()
    if not archive.has_key(year):
        abort(404)
    if not archive[year].has_key(month):
        abort(404)
    return render_template('archive_month.html',
        archive=archive[year][month],
        year=year,
        month=month
    )

def setup(app, cfg):
    app.register_blueprint(archive)