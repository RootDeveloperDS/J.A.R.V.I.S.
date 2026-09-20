# Plugin Base Format (every plugin should have this)

#def run_calculator(command_text, output_widget):
   # output_widget.insert("end", "🧮 Calculator plugin coming soon!\n")
   # output_widget.see("end")

# plugins/calculator.py

import re
import ast
import operator
from voice.tts import speak

def safe_eval(expr):
    """
    Safely evaluate a mathematical expression using AST.
    """
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            op = type(node.op)
            if op not in allowed_operators:
                raise ValueError(f"Unsupported operator: {op}")
            return allowed_operators[op](evaluate(node.left), evaluate(node.right))
        elif isinstance(node, ast.UnaryOp):
            op = type(node.op)
            if op not in allowed_operators:
                raise ValueError(f"Unsupported operator: {op}")
            return allowed_operators[op](evaluate(node.operand))
        else:
            raise ValueError(f"Unsupported expression type: {type(node)}")

    try:
        tree = ast.parse(expr, mode='eval')
        return evaluate(tree.body)
    except Exception:
        return None

def register():
    return {
        "trigger": "calculator",
        "description": "Performs math calculations",
        "run": run_calculator
    }

def run_calculator(command, output_widget):
    result = perform_calculation(command)

    if result is not None:
        response = f"Result: {result}"
    else:
        response = "⚠️ Sorry, I couldn’t calculate that."

    output_widget.insert("end", response + "\n")
    output_widget.see("end")
    speak(response)


def perform_calculation(command):
    expression = command.lower()

    # Handle specific English phrases manually
    if "subtract" in expression and "from" in expression:
        try:
            parts = re.findall(r'\d+', expression)
            if len(parts) == 2:
                return int(parts[1]) - int(parts[0])
        except:
            return None

    if "divide" in expression and "by" in expression:
        try:
            parts = re.findall(r'\d+', expression)
            if len(parts) == 2:
                return int(parts[0]) / int(parts[1])
        except:
            return None


    # 1️⃣ Handle: "increase A by B%"
    inc_match = re.search(r'increase (\d+(?:\.\d+)?) by (\d+(?:\.\d+)?)%', expression)
    if inc_match:
        base = float(inc_match.group(1))
        percent = float(inc_match.group(2))
        return base + (base * percent / 100)

    # 2️⃣ Handle: "decrease A by B%"
    dec_match = re.search(r'decrease (\d+(?:\.\d+)?) by (\d+(?:\.\d+)?)%', expression)
    if dec_match:
        base = float(dec_match.group(1))
        percent = float(dec_match.group(2))
        return base - (base * percent / 100)

    # 3️⃣ Handle: "X% of Y"
    of_match = re.search(r'(\d+(?:\.\d+)?)% of (\d+(?:\.\d+)?)', expression)
    if of_match:
        percent = float(of_match.group(1))
        base = float(of_match.group(2))
        return (percent / 100) * base

    # 4️⃣ Handle: "A plus B%" → 100 + 10% = 110
    plus_percent = re.search(r'(\d+(?:\.\d+)?) plus (\d+(?:\.\d+)?)%', expression)
    if plus_percent:
        base = float(plus_percent.group(1))
        percent = float(plus_percent.group(2))
        return base + (base * percent / 100)

    # 5️⃣ Replace keyword math
    replacements = {
        "plus": "+", "add": "+",
        "minus": "-", "subtract": "-",
        "times": "*", "multiply": "*",
        "divided by": "/", "divide": "/",
        "mod": "%", "modulus": "%",
        "power": "**"
    }
    for word, symbol in replacements.items():
        expression = expression.replace(word, symbol)

    # 6️⃣ Extract standard math expressions
    match = re.findall(r'[-+*/%()0-9.\s]+', expression)
    if match:
        try:
            clean_expr = "".join(match).strip()
            return safe_eval(clean_expr)
        except:
            return None
    return None

if __name__ == "__main__":
    # Tests for safe math evaluation
    assert safe_eval("2 + 2") == 4
    assert safe_eval("10 - 5") == 5
    assert safe_eval("3 * 4") == 12
    assert safe_eval("10 / 2") == 5
    assert safe_eval("10 % 3") == 1
    assert safe_eval("2 ** 3") == 8
    assert safe_eval("(2 + 3) * 4") == 20
    assert safe_eval("-5 + 10") == 5
    assert safe_eval("+5") == 5

    # Tests for malicious / invalid expressions
    assert safe_eval("__import__('os').system('echo hacked')") is None
    assert safe_eval("print('hello')") is None
    assert safe_eval("open('test.txt', 'w')") is None

    print("All calculator tests passed!")
