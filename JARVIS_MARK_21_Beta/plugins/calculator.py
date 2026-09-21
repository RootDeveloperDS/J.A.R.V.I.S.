# plugins/calculator.py

import re
from voice.tts import speak
from core.base_plugin import BasePlugin


class CalculatorPlugin(BasePlugin):
    name = "Calculator Plugin"
    trigger = "calculator"
    description = "Performs advanced math calculations via voice/text"
    version = "2.0.0"

    def run(self, command: str, output_widget):
        result = perform_calculation(command)
        if result is not None:
            response = f"Result: {result}"
        else:
            response = "⚠️ Sorry, I couldn't calculate that."

        if output_widget:
            output_widget.insert("end", response + "\n")
            output_widget.see("end")
        speak(response)


# Legacy register fallback
def register():
    return {
        "trigger": "calculator",
        "description": "Performs math calculations",
        "run": run_calculator
    }


def run_calculator(command, output_widget):
    plugin = CalculatorPlugin()
    plugin.run(command, output_widget)


def perform_calculation(command):
    expression = command.lower()

    # Handle specific English phrases manually
    if "subtract" in expression and "from" in expression:
        try:
            parts = re.findall(r'\d+', expression)
            if len(parts) == 2:
                return int(parts[1]) - int(parts[0])
        except Exception:
            return None

    if "divide" in expression and "by" in expression:
        try:
            parts = re.findall(r'\d+', expression)
            if len(parts) == 2:
                return int(parts[0]) / int(parts[1])
        except Exception:
            return None

    # Handle percentage calculation
    inc_match = re.search(r'increase (\d+(?:\.\d+)?) by (\d+(?:\.\d+)?)%', expression)
    if inc_match:
        base = float(inc_match.group(1))
        percent = float(inc_match.group(2))
        return base + (base * percent / 100)

    dec_match = re.search(r'decrease (\d+(?:\.\d+)?) by (\d+(?:\.\d+)?)%', expression)
    if dec_match:
        base = float(dec_match.group(1))
        percent = float(dec_match.group(2))
        return base - (base * percent / 100)

    of_match = re.search(r'(\d+(?:\.\d+)?)% of (\d+(?:\.\d+)?)', expression)
    if of_match:
        percent = float(of_match.group(1))
        base = float(of_match.group(2))
        return (percent / 100) * base

    plus_percent = re.search(r'(\d+(?:\.\d+)?) plus (\d+(?:\.\d+)?)%', expression)
    if plus_percent:
        base = float(plus_percent.group(1))
        percent = float(plus_percent.group(2))
        return base + (base * percent / 100)

    # Replace keyword math
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

    # Extract standard math expressions
    match = re.findall(r'[-+*/%()0-9.\s]+', expression)
    if match:
        try:
            clean_expr = "".join(match).strip()
            return eval(clean_expr, {"__builtins__": None}, {})
        except Exception:
            return None
    return None
