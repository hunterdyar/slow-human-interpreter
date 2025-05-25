import unittest

from interpreter.Interpreter import interpret


class TestCompiler(unittest.TestCase):
    def test_empty(self):
        x = interpret("")
        self.assertNotEqual(x, None)

    def test_print(self):
        x = interpret("print(\"hi\")")
        self.assertNotEqual(x, None)

    def test_add(self):
        x = interpret("1+3")
        print(x)
        self.assertEqual(1, len(x.routines))
        self.assertEqual(3, len(x.routines["main"].instructions))
