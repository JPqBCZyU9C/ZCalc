"""Lógica de cálculo independiente de la interfaz gráfica."""

import ast
import re
from decimal import Decimal, DivisionByZero, InvalidOperation, localcontext


class Calculator:
    OPERATORS = "+-*/"

    def __init__(self):
        self.clear()

    def clear(self):
        self.expression = "0"
        self.history = ""
        self.error = ""
        self.finished = False

    @property
    def screen(self):
        if self.error:
            return self.error
        return self.expression.translate(str.maketrans({"*": "×", "/": "÷", "-": "−"}))

    def press(self, key):
        if key == "C":
            self.clear()
            return

        if self.error:
            if key not in "0123456789.":
                return
            self.clear()

        if key in "0123456789" and len(key) == 1:
            self._digit(key)
        elif key == ".":
            self._decimal_point()
        elif key in self.OPERATORS and len(key) == 1:
            self._operator(key)
        elif key == "⌫":
            self.expression = self.expression[:-1] or "0"
            self.finished = False
            self.history = ""
        elif key == "±":
            self._toggle_sign()
        elif key == "%":
            self._percent()
        elif key == "=":
            self._calculate()

    def _prepare_number(self):
        if self.finished:
            self.expression = "0"
            self.history = ""
            self.finished = False

    def _digit(self, digit):
        self._prepare_number()
        match = re.search(r"\d+(?:\.\d*)?$", self.expression)
        if match and match.group() == "0":
            self.expression = self.expression[:match.start()] + digit
        elif self.expression == "0":
            self.expression = digit
        else:
            self.expression += digit
        if len(self.expression) > 80:
            self.expression = self.expression[:-1]

    def _decimal_point(self):
        self._prepare_number()
        tail = re.search(r"\d*(?:\.\d*)?$", self.expression).group()
        if "." in tail:
            return
        if not tail:
            self.expression += "0."
        else:
            self.expression += "."

    def _operator(self, operator):
        self.finished = False
        if self.expression == "0" and operator == "-":
            self.expression = "-"
            return
        if self.expression == "-":
            return
        if self.expression[-1] in self.OPERATORS:
            self.expression = self.expression[:-1] + operator
        else:
            if self.expression.endswith("."):
                self.expression += "0"
            self.expression += operator

    def _toggle_sign(self):
        if self.finished:
            self.finished = False
            self.history = ""
        match = re.search(r"\d+(?:\.\d*)?$", self.expression)
        if not match:
            return
        start = match.start()
        if start and self.expression[start - 1] == "-" and (
            start == 1 or self.expression[start - 2] in self.OPERATORS
        ):
            self.expression = self.expression[:start - 1] + self.expression[start:]
        else:
            self.expression = self.expression[:start] + "-" + self.expression[start:]

    def _percent(self):
        match = re.search(r"\d+(?:\.\d*)?$", self.expression)
        if not match:
            return
        number = Decimal(match.group()) / Decimal(100)
        self.expression = self.expression[:match.start()] + self._format(number)
        self.finished = False

    def _calculate(self):
        if self.expression[-1] in self.OPERATORS + ".":
            return
        try:
            with localcontext() as context:
                context.prec = 28
                value = self._evaluate(ast.parse(self.expression, mode="eval").body)
            result = self._format(value)
            self.history = self.screen + " ="
            self.expression = result
            self.finished = True
        except (ZeroDivisionError, DivisionByZero):
            self.error = "División entre cero"
        except (SyntaxError, InvalidOperation, OverflowError, ValueError, TypeError):
            self.error = "Error de cálculo"

    @classmethod
    def _evaluate(cls, node):
        # Únicamente se aceptan números y operaciones aritméticas básicas.
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return Decimal(str(node.value))
        if isinstance(node, ast.UnaryOp):
            operand = cls._evaluate(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
            if isinstance(node.op, ast.UAdd):
                return operand
        if isinstance(node, ast.BinOp):
            left = cls._evaluate(node.left)
            right = cls._evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError
                return left / right
        raise ValueError("Operación no admitida")

    @staticmethod
    def _format(value):
        if not value.is_finite():
            raise InvalidOperation
        normalized = value.normalize()
        result = format(normalized, "f")
        if len(result) > 22:
            result = format(normalized, ".12g")
        return "0" if result in ("-0", "") else result
