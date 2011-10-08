# -*- coding: utf-8 -*-
"""
    flask-rst.test_flaskrst.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import os
import os.path
import unittest

from flaskext.testing import TestCase
from flaskrst import app, set_source

class SimpleTest(TestCase):
    TESTING = True

    def create_app(self):
        set_source(app, source_path=os.path.join(os.getcwd(),
                                                 '../example/'))
        return app

    def test_index(self):
        rv = self.client.get('/')
        self.assert_200(rv)
        assert "A very simple blog post" in rv.data

    def test_year_ok(self):
        rv = self.client.get('/2011/')
        self.assert_200(rv)

    def test_year_fail(self):
        rv = self.client.get('/2010/')
        self.assert_404(rv)

    def test_month_ok(self):
        rv = self.client.get('/2011/10/')
        self.assert_200(rv)

    def test_post(self):
        rv = self.client.get('/2011/10/4/hello-world/')
        self.assert_200(rv)
        assert "This is my first blog post with" in rv.data

    def test_archive(self):
        rv = self.client.get('/archive/')
        self.assert_200(rv)

    def test_tags_index(self):
        rv = self.client.get('/tags/')
        self.assert_200(rv)

    def test_tags_hello(self):
        rv = self.client.get('/tags/hello/')
        self.assert_200(rv)
        assert "Hello World" in rv.data

    def test_about(self):
        rv = self.client.get('/about/')
        self.assert_200(rv)
        assert "This is a example for a simple static page." in rv.data



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleTest))
    return suite


if __name__ == '__main__':
    unittest.main()
