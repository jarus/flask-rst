# -*- coding: utf-8 -*-
"""
    flask-rst.modules.disqus
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""


from flask import render_template, request
from jinja2 import Markup

disqus_config = {}

def template_comments(doc=object()):
    disqus = {
        'shortname': disqus_config['shortname'],
        'url': request.base_url,
    }
    
    if hasattr(doc, "title"):
        disqus['title'] = doc.title

    return Markup(
        render_template("disqus_comments.html", disqus=disqus)
    )

def setup(app, cfg):
    global disqus_config
    disqus_config = cfg
    if 'shortname' not in disqus_config:
        raise RuntimeError("Missing 'shortname' config key in disqus config")
    
    app.jinja_env.globals['comments'] = template_comments