# -*- coding: utf-8 -*-
"""
    flask-rst.modules
    ~~~~~~~~~~~~~~~~~

    Module interface inspired by Armin Ronacher rstblog. 

    :copyright: (c) 2011 by Christoph Heer
    :license: BSD, see LICENSE for more details.
"""

import sys

OLD_MODULES_NAMES = ('archive', 'atom', 'blog', 'page', 'pygments', 'tags') 

class FlaskRSTModuleManager(object):
    
    loaded_modules = {} 
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
    
    def _import(self, module_name):
        __import__(module_name)
        return sys.modules[module_name]
    
    def load(self, module_name, module_cfg):
        if module_name in self.loaded_modules:
            return False
        
        if module_name in OLD_MODULES_NAMES:
            module_name = 'flaskrst.modules.' + module_name
            
        module = self._import(module_name)
        if not hasattr(module, "setup"):
            raise ImportError("flask-rst module %s hasn't a setup function" % 
                              module_name)

        module.setup(self.app, module_cfg)
        
        self.loaded_modules[module_name] = module
        return True
    
    def load_from_config(self):
        for module_name, module_cfg in self.app.config['MODULES'].items():
            if not module_cfg.get('active', True):
                continue
            self.load(module_name, module_cfg)

    def __contains__(self, obj):
        return obj in self.loaded_modules

    def __getitem__(self, name):
        return self.loaded_modules[name]

manager = FlaskRSTModuleManager()