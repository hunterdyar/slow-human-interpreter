import unittest

from interpreter.Interpreter import interpret
from printer.printer import create_html_file


class TestPrinter(unittest.TestCase):
    def test_empty(self):
        x = interpret("1+2 > 3*4")
        create_html_file(x)