import unittest

from interpreter.Interpreter import interpret
from printer.printer import create_html_file


class TestPrinter(unittest.TestCase):
    def test_empty(self):
        x = interpret("1+2 > 3*4")
        create_html_file(x)

    def test_jumps(self):
        x = interpret("""
if False:
    print("banana")
elif False:
    print("cheese")
elif False:
    print("cheese")
else:
    print("cake")
""")
        create_html_file(x)

class TestPrinter2(unittest.TestCase):
    def test_empty(self):
        x = interpret("1+2 > 3*4")
        create_html_file(x)

    def test_functon_defs(self):
        x = interpret("""
def do_something_awesome(a,b):
    print(a)
    print(b)


do_something_awesome(1,2+4)
""")
        create_html_file(x)