import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def enter(self, keys):
        for key in keys:
            self.calc.press(key)
        return self.calc.screen

    def test_basic_operations(self):
        for keys, expected in (
            ("12+7=", "19"),
            ("9-4=", "5"),
            ("8*6=", "48"),
            ("9/2=", "4.5"),
        ):
            self.calc.clear()
            self.assertEqual(self.enter(keys), expected)

    def test_precedence(self):
        self.assertEqual(self.enter("2+3*4="), "14")

    def test_decimals(self):
        self.assertEqual(self.enter("0.1+0.2="), "0.3")

    def test_divide_by_zero(self):
        self.assertEqual(self.enter("8/0="), "División entre cero")
        self.assertEqual(self.enter("3"), "3")

    def test_zero_divided_by_zero(self):
        self.assertEqual(self.enter("0/0="), "División entre cero")

    def test_clear_and_backspace(self):
        self.assertEqual(self.enter("123⌫"), "12")
        self.assertEqual(self.enter("C"), "0")

    def test_percent(self):
        self.assertEqual(self.enter("50%"), "0.5")

    def test_sign(self):
        self.assertEqual(self.enter("5±"), "−5")
        self.assertEqual(self.enter("±"), "5")

    def test_continue_after_equals(self):
        self.assertEqual(self.enter("4+2=+3="), "9")

    def test_new_number_after_equals(self):
        self.assertEqual(self.enter("4+2=9"), "9")

    def test_zero_replacement(self):
        self.assertEqual(self.enter("5+03="), "8")

    def test_unary_sign_after_operator(self):
        self.assertEqual(self.enter("5+3±="), "2")

    def test_no_execution_of_unexpected_expressions(self):
        with self.assertRaises(ValueError):
            Calculator._evaluate(__import__("ast").parse("f()", mode="eval").body)


if __name__ == "__main__":
    unittest.main()
