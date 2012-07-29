# -*- coding: utf-8 -*-
"""
    flaskrst.modules.pygments
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import time

from docutils import nodes
from docutils.parsers.rst import Directive

from flask import render_template

try:
    import requests
except ImportError:
    import sys
    sys.exit("To use github in flask-rst you must install requests")

_github_repo_cache = {}

class GitHubRepoDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    
    def run(self):
        repo = self.arguments[0]

        if repo in _github_repo_cache \
        and _github_repo_cache[repo]['expire'] > time.time():
            html = _github_repo_cache[repo]['html']
        else:
            headers = {}
            if repo in _github_repo_cache:
                headers['If-None-Match'] = _github_repo_cache[repo]['etag']
            
            res = requests.get(
                'https://api.github.com/repos/%s' % repo, 
                headers=headers
            ) 
            
            if res.status_code == 304:
                html = _github_repo_cache[repo]['html']
                
                _github_repo_cache[repo]['expire'] = time.time() + 600
            elif res.status_code == 200:
                html = render_template('github_repo.html', repo=res.json)
                
                _github_repo_cache[repo] = {}
                _github_repo_cache[repo]['html'] = html
                _github_repo_cache[repo]['expire'] = time.time() + 600
                _github_repo_cache[repo]['etag'] = res.headers.get('ETag')
            else:
                raise self.error("GitHub API error: %s" % res.json['message'])
                            
        return [nodes.raw('', html, format='html')]
    
def setup(app, cfg):
    from docutils.parsers.rst import directives
    directives.register_directive('github-repo', GitHubRepoDirective)