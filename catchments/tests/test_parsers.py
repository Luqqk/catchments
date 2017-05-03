from unittest import TestCase
from optparse import OptionParser
from catchments.parsers import create_skobbler_parser, create_here_parser


# Run tests with:
# coverage run --branch --source=catchments/ setup.py test
# To check coverage report (with missing lines)
# coverage report -m


class TestParsers(TestCase):

    def test_create_skobbler_parser(self):
        parser = create_skobbler_parser()
        self.assertTrue(isinstance(parser, OptionParser))

    def test_create_here_parser(self):
        parser = create_here_parser()
        self.assertTrue(isinstance(parser, OptionParser))
