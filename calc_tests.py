import unittest
import sys
import calc
from io import StringIO

class TestCalc(unittest.TestCase):

    def setUp(self):
        self.calc = calc.Calculator()

    def test_valid_command(self):
        self.assertTrue(self.calc.valid_command("quit"))
        self.assertTrue(self.calc.valid_command("Quit")) # case insensitive
        self.assertFalse(self.calc.valid_command("??"))

        # should not be able to print before added, this is how I assumed it should work
        self.assertFalse(self.calc.valid_command("print a"))
        # should be able to print added (mentioned before) register
        self.calc.add_register("a")
        self.assertTrue(self.calc.valid_command("print a")) 
        self.assertFalse(self.calc.valid_command("pr1nt a"))

        # operation tests
        self.calc.add_register("b")
        self.assertTrue(self.calc.valid_command("a add b"))
        self.assertTrue(self.calc.valid_command("d add c"))
        self.assertFalse(self.calc.valid_command("d asd 1"))
        self.assertTrue(self.calc.valid_command("d multiply 1"))
        self.assertTrue(self.calc.valid_command("d subtract 1"))

    def test_case_pdf(self):
        # from the pdf
        s1 = StringIO("A add 2\nA add 3\nprint A\nB add 5\nB subtract 2\nprint B\nA add 1\nprint A\nquit")
        actual = self.calc.handle_input(s1)
        expected = [5, 3, 6]
        self.assertListEqual(actual, expected)

        s2 = StringIO("result add revenue\nresult subtract costs\nrevenue add 200\ncosts add salaries\nsalaries add 20\nsalaries multiply 5\ncosts add 10\nprint result\nQUIT\n")
        actual = self.calc.handle_input(s2)
        expected = [90]
        self.assertListEqual(actual, expected)

    def test_cycle(self):
        input = StringIO("r1 add r2\nr2 add r3\nr3 add r1\nr3 add r1")

        # r1 -> r2 -> r3
        # should not be possible to add r3 to r1
        # should not be possible to add r1 to r3
        # this is because they are already dependent of eachother in some way.
        # I assume the calculator should work in this way atleast.

        actual = self.calc.handle_input(input)
        expected = ["r3 add r1", "r3 add r1"] # two last commands should fail and thus be printed
        self.assertListEqual(actual, expected)

    def test_add_itself(self):
        input = StringIO("r add r")
        actual = self.calc.handle_input(input)
        expected = ["r add r"]
        self.assertListEqual(actual, expected)

unittest.main()