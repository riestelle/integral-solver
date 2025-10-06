import math
from sympy import symbols, integrate, sympify
import re
x = symbols('x') 

def add(numbers):
    return sum(map(float, numbers))

def sub(numbers):
    nums = list(map(float, numbers))
    return nums[0] - sum(nums[1:])

def multiply(numbers):
    result = 1
    for num in map(float, numbers):
        result *= num
    return result

def divide(numbers):
    nums = list(map(float, numbers))
    try:
        result = nums[0]
        for n in nums[1:]:
            result /= n
        return result
    except ZeroDivisionError:
        return "Division by zero error"

def find_sqrt(numbers):
    return [math.sqrt(float(n)) for n in numbers]

def cube_root(numbers):
    return [float(n) ** (1/3) for n in numbers]

def power(numbers):
    if len(numbers) >= 2:
        base = float(numbers[0])
        exponent = float(numbers[1])
        return base ** exponent
    return "Need base and exponent"

def square(numbers):
    return [float(n) ** 2 for n in numbers]

def cube(numbers):
    return [float(n) ** 3 for n in numbers]

def fact(numbers):
    results = []
    for num in numbers:
        try:
            n = int(float(num))
            results.append(math.factorial(n))
        except:
            results.append(f"Invalid input: {num}")
    return results

def sin_value(numbers):
    return [math.sin(math.radians(float(n))) for n in numbers]

def sinh_value(numbers):
    return [math.sinh(float(n)) for n in numbers]

def cos_value(numbers):
    return [math.cos(math.radians(float(n))) for n in numbers]

def cosh_value(numbers):
    return [math.cosh(float(n)) for n in numbers]

def tan_value(numbers):
    return [math.tan(math.radians(float(n))) for n in numbers]

def tanh_value(numbers):
    return [math.tanh(float(n)) for n in numbers]

def log(numbers):
    try:
        num = float(numbers[0])
        base = float(numbers[1])
        return math.log(num, base)
    except:
        return "Invalid input for logarithm"


def symbolic_integral(command):
    try:
        expr_text = command.lower()
        expr_text = expr_text.replace("integrate", "")
        expr_text = expr_text.replace("integral of", "")
        expr_text = expr_text.replace("the", "")
        expr_text = expr_text.replace("squared", "**2")
        expr_text = expr_text.replace("cubed", "**3")
        expr_text = expr_text.replace("to the power of", "**")
        expr_text = expr_text.replace("times", "*")
        expr_text = expr_text.replace("multiply", "*")
        expr_text = expr_text.replace("plus", "+")
        expr_text = expr_text.replace("minus", "-")
        expr_text = expr_text.replace("open parenthesis", "(")
        expr_text = expr_text.replace("close parenthesis", ")")

        expr_text = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expr_text)
        expr_text = re.sub(r"([a-zA-Z])(\d)", r"\1*\2", expr_text)
        expr_text = re.sub(r"\bsin\s+([a-zA-Z0-9]+)", r"sin(\1)", expr_text)
        expr_text = re.sub(r"\bcos\s+([a-zA-Z0-9]+)", r"cos(\1)", expr_text)
        expr_text = re.sub(r"\btan\s+([a-zA-Z0-9]+)", r"tan(\1)", expr_text)

        expr_text = expr_text.strip()
        expr = sympify(expr_text)
        result = integrate(expr, x)
        return f"∫ {expr} dx = {result} + C"
    except Exception as e:
        return f"Sorry, I couldn't compute the integral. Error: {e}"