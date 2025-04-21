import pytest

from calculator.parser import Number, BinaryOp, parse

from calculator.evaluator import evaluate
import math

@pytest.mark.parametrize("expr, result", [
    (BinaryOp(Number(1), '+', Number(2)), 3),
    (BinaryOp(Number(4), '-', Number(2)), 2),
    (BinaryOp(Number(3), '*', Number(5)), 15),
    (BinaryOp(Number(10), '/', Number(2)), 5),
])
def test_simple_evaluations(expr, result):
    assert evaluate(expr) == result

def test_nested_expression():
    expr = BinaryOp(Number(2), '+', BinaryOp(Number(3), '*', Number(4)))  
    assert evaluate(expr) == 14

def test_division_by_zero():
    expr = BinaryOp(Number(1), '/', Number(0))
    with pytest.raises(ZeroDivisionError):
        evaluate(expr)

def test_large_division():
    expr = BinaryOp(Number(1e300), '/', Number(1e-300))
    with pytest.raises(OverflowError):
        evaluate(expr)

def test_unknown_operator():
    expr = BinaryOp(Number(1), '%', Number(2))  
    with pytest.raises(ValueError):
        evaluate(expr)

def test_basic_math():
    assert evaluate(parse("1 + 1")) == 2
    assert evaluate(parse("2 * 3")) == 6

def test_exponent():
    assert evaluate(parse("2^3")) == 8

def test_scientific():
    assert evaluate(parse("1.25e2")) == 125.0

def test_parentheses():
    result = evaluate(parse("1 + 2 / (3 + 4)"))
    assert abs(result - 1.2857142857142856) < 1e-10

def test_floating_point_sum():
    result = evaluate(parse("0.1 + 0.2"))
    assert abs(result - 0.3) < 1e-9  

def test_near_zero_division():
    expr = "1 / 1e-300"
    result = evaluate(parse(expr))
    assert result > 1e+299

def test_negative_exponent():
    assert evaluate(parse("4^-2")) == 0.0625

def test_constants():
    assert abs(evaluate(parse("pi")) - math.pi) < 0.01
    assert abs(evaluate(parse("e")) - math.e) < 0.01

def test_functions():
    assert abs(evaluate(parse("sin(pi / 2)")) - 1) < 0.01
    assert abs(evaluate(parse("cos(0)")) - 1) < 0.01
    assert abs(evaluate(parse("tg(pi / 4)")) - 1) < 0.01
    assert abs(evaluate(parse("ctg(pi / 4)")) - 1) < 0.01
    assert abs(evaluate(parse("ln(e)")) - 1) < 0.01
    assert abs(evaluate(parse("exp(1)")) - 2.718281828459045) < 0.01
    assert abs(evaluate(parse("sqrt(4)")) - 2) < 0.01
    assert abs(evaluate(parse("pi")) - 3.141592653589793) < 0.01
    assert abs(evaluate(parse("e")) - 2.718281828459045) < 0.01
    assert abs(evaluate(parse("sqrt(ln(e))")) - 1) < 0.01
