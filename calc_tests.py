import unittest
import sys
import calc


class TestCalc(unittest.TestCase):

    def test_valid_command(self):
        self.assertTrue(calc.valid_command("quit"))
        self.assertTrue(calc.valid_command("Quit")) # case insensitive
        self.assertFalse(calc.valid_command("??"))

        # should not be able to print before added, this is how I assumed it should work
        self.assertFalse(calc.valid_command("print a"))
        # should be able to print added (mentioned before) register
        calc.add_register("a")
        self.assertTrue(calc.valid_command("print a")) 
        self.assertFalse(calc.valid_command("pr1nt a"))

        # operation tests
        calc.add_register("b")
        self.assertTrue(calc.valid_command("a add b"))
        self.assertTrue(calc.valid_command("a add c"))
        self.assertTrue(calc.valid_command("d add c"))
        self.assertTrue(calc.valid_command("d add 1"))
        self.assertFalse(calc.valid_command("d asd 1"))
        self.assertTrue(calc.valid_command("d multiply 1"))
        self.assertTrue(calc.valid_command("d subtract 1"))

    def test_case_1(self):
        t1 = open('test1.txt', 'r')
        output = calc.handle_input(t1)
        t1.close()
        self.assertEquals(output, "80")


unittest.main()