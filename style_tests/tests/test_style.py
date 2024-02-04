"""Testing the style of the style checking code."""

import sys
import unittest

import typeguard

with typeguard.install_import_hook("style_tests"):
    import style_tests


class TestStyle(unittest.TestCase, style_tests.TestStyle):
    """Testing the style of the package and tests code."""

    modules = [
        style_tests,
        sys.modules[__name__.split(".", 1)[0]],
    ]
