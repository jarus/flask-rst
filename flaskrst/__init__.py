# -*- coding: utf-8 -*-
"""
    flask-rstblog
    ~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
from datetime import date

from jinja2 import FileSystemLoader
from flask import Flask, render_template

from flaskrst.modules import manager, FlaskRSTModuleManager
from flaskrst.templating import inject_navigation, inject_default_stylesheet

class Flask(Flask):
    def create_global_jinja_loader(self):
        template_path = os.path.join(self.config.get('SOURCE', ''),
                                     "_templates")
        builtin_templates = os.path.join(self.root_path, self.template_folder)
        return FileSystemLoader([template_path, builtin_templates])

def create_app(source=None, config=None):    
    app = Flask("flaskrst")
    
    # Set default config values
    app.config.setdefault('MODULES', {})
    app.config.setdefault('STYLESHEETS', [])
    app.config.setdefault('FEEDS', [])
    
    # Load config
    if config:
        app.config.from_pyfile(config)
        config_loaded = True
    # maybe there is a file declared by env
    elif 'FLASK_RST_CONFIG' in os.environ:
        app.config.from_envvar('FLASK_RST_CONFIG')
        config_loaded = True
    # no config loaded try again later after source setting
    else:
        config_loaded = False
    
    # Set source path
    if source:
        app.config['SOURCE'] = source
    elif 'FLASK_RST_SOURCE' in os.environ:
        app.config['SOURCE'] = os.environ['FLASK_RST_SOURCE']
    else:
        # Use current working directory as source
        app.config['SOURCE'] = os.getcwd()
    
    # If no config already loaded than is a config maybe in source path
    if not config_loaded:
        config_path = os.path.join(app.config['SOURCE'], 'config.py')
        app.config.from_pyfile(config_path, silent=True)
    
    # Set path of static folder
    if 'STATIC_FOLDER' in app.config:
        app.static_folder = app.config['STATIC_FOLDER']
    else:
        # Is a static folder called _static in source path?
        source_static_folder = os.path.join(app.config['SOURCE'], "_static")
        if os.path.isdir(source_static_folder):
            app.static_folder = source_static_folder
    
    # Load flask-rst modules
    manager.init_app(app)
    manager.load_from_config()

    # Add some jinja globals and context processors
    app.jinja_env.globals['date'] = date
    app.context_processor(inject_navigation)
    
    # Inject the default stylesheet 'style.css' is there no other stylesheet 
    # in app config
    inject_default_stylesheet(app)
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app