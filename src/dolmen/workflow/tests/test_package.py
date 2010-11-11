# -*- coding: utf-8 -*-

import unittest
import pkg_resources
from dolmen.workflow import tests
from zope.testing import doctest


def make_test(dottedname):
    test = doctest.DocTestSuite(
        dottedname, setUp=tests.siteSetUp, tearDown=tests.siteTearDown,
        optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    test.layer = tests.TestLayer(tests)
    return test


def suiteFromPackage(name):
    files = pkg_resources.resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'dolmen.workflow.tests.%s.%s' % (name, filename[:-3])
        suite.addTest(make_test(dottedname))
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['components',]:
        suite.addTest(suiteFromPackage(name))
    return suite
