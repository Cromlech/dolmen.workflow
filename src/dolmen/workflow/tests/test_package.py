# -*- coding: utf-8 -*-

import doctest
import unittest
import pkg_resources


def make_test(dottedname):
    test = doctest.DocTestSuite(
        dottedname,
        optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
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
