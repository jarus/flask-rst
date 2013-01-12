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
    sys.exit("To use github in flask-rst you must install requests>=1.0.0")


def get_json_from_response(res):
    """
    This is only a stupid function to support requests befor and
    after 1.0.0.0
    """

    if requests.__version__ < '1.0.0':
        return res.json
    else:
        return res.json()


class GitHubAPIException(Exception):

    message = "unknow"

    def __init__(self, message):
        self.message = message


class GitHubRepoCache():

    _cache = {}

    def __getitem__(self, repo):
        if repo not in self._cache \
        or self._cache[repo]['expire'] < time.time():
            headers = {}
            if repo in self._cache:
                headers['If-None-Match'] = self._cache[repo]['etag']

            res = requests.get(
                'https://api.github.com/repos/%s' % repo,
                headers=headers
            )

            if res.status_code == 304:
                self._cache[repo]['expire'] = time.time() + 600
            elif res.status_code == 200:
                self._cache[repo] = {}
                self._cache[repo]['expire'] = time.time() + 600
                self._cache[repo]['etag'] = res.headers.get('ETag')
                self._cache[repo]['json'] = get_json_from_response(res)
            else:
                raise GitHubAPIException(get_json_from_response(res))

        return self._cache[repo]['json']


github_repo_cache = GitHubRepoCache()


class GitHubRepoDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        repo = self.arguments[0]

        try:
            repo_json = github_repo_cache[repo]
        except GitHubAPIException, e:
            raise self.error("GitHub API error: %s" % e.message)

        html = render_template('github_repo.html', repo=repo_json)
        return [nodes.raw('', html, format='html')]


def setup(app, cfg):
    from docutils.parsers.rst import directives
    directives.register_directive('github-repo', GitHubRepoDirective)
