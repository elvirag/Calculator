import re
from collections import deque

variable_dict = {}


def str_to_num(a):
    try:
        a = float(a)
        if a % 1 < 0.0001:
            return int(a)
        if a.is_integer():
            return int(a)
    except OverflowError:
        return int(a)

    return a


def parse_input(input_line):
    """This function parses input according to all symbols,
    when plus and minus are allowed to be several adjacent, and other signs are not.
    The loop goes through the elements and converts chains of minus or pluses
    into a s single element of minus or plus.
    The function then returns the list of elements."""
    elements = re.findall(r"(-*\d*\.\d+|-*\d+|[a-zA-Z]+|-+|\++|[*/^()])", input_line)
    elements = [element for element in elements if element]

    for ind, element in enumerate(elements):
        if len(element) == element.count("+") + element.count("-"):
            if "-" in element or "+" in element:
                if element.count("-") % 2 == 1:
                    elements[ind] = "-"
                else:
                    elements[ind] = "+"

    return elements


def check_variable_valid_assignment(variable):
    try:
        return str_to_num(variable)
    except ValueError:
        if not variable.isalpha():
            return "Invalid assignment"
        if variable not in variable_dict:
            return "Unknown variable"

        return variable_dict[variable]


def calculate_postfix(postfix):
    calculation_stack = deque()
    if postfix:
        for element in postfix:
            if element in ["/", "*", "-", "+", "^"]:
                a = calculation_stack.pop()
                b = calculation_stack.pop()
                if element == "/":
                    if a == 0:
                        return "Division by zero"
                    calculation_stack.append(b / a)
                elif element == "*":
                    calculation_stack.append(a * b)
                elif element == "+":
                    calculation_stack.append(a + b)
                elif element == "-":
                    calculation_stack.append(b - a)
                else:
                    calculation_stack.append(a ** b)
            else:
                calculation_stack.append(element)
    else:
        return "Nothing was input"

    return str_to_num(calculation_stack[-1])


def is_operand(symbol):
    return symbol not in "+-/*^()"


def infix_to_postfix(symbols):
    postfix_stack = deque()
    postfix = []
    precedences = {'(': 0, "+": 1, '-': 1, '*': 2, '/': 2, '^': 3}

    for symbol in symbols:
        if is_operand(symbol):
            res = check_variable_valid_assignment(symbol)
            if isinstance(res, int) or isinstance(res, float):
                postfix.append(res)
            else:
                return res
        elif symbol == "(":
            postfix_stack.append(symbol)
        elif symbol == ")":
            top = postfix_stack.pop()
            while top != "(":
                postfix.append(top)
                top = postfix_stack.pop()
        elif not postfix_stack or postfix_stack[-1] == "(":
            postfix_stack.append(symbol)
        else:
            while postfix_stack and precedences[postfix_stack[-1]] >= precedences[symbol]:
                postfix += postfix_stack.pop()
            postfix_stack.append(symbol)

    while postfix_stack:
        postfix += postfix_stack.pop()

    # syntax error
    if postfix_stack:
        return "Invalid expression"

    return postfix


def solve(input_line):
    symbols = parse_input(input_line)
    postfix = infix_to_postfix(symbols)
    if postfix not in ["Invalid expression", "Invalid assignment", "Unknown variable"]:
        res = calculate_postfix(postfix)
        return res

    return postfix


def validate_identifiers(input_line):
    m = re.search(r"\s*[A-Za-z]+[0-9]+|[0-9]+[A-Za-z]+\s*=", input_line)
    if m is not None:
        return "Invalid identifier"

    return


def validate_expression(input_line):
    """This function handles not paired brackets, adjacent mul/dic signs and too many assignment symbols"""

    m = re.search(r"([*]{2,}|[/]{2,}|[\^]{2,})", input_line)
    paren = input_line.count("(") - input_line.count(")")
    if not (m is None and paren == 0):
        return "Invalid expression"
    if input_line.count("=") > 1:
        return "Invalid assignment"

    return


def calculator():
    user_input = input()
    if user_input == "":
        return ""
    if not user_input.startswith("/"):
        res = validate_expression(user_input)
        if res:
            return res
        res = validate_identifiers(user_input)
        if res:
            return res

        left_val = None
        if "=" in user_input:
            left_val = user_input.split("=")[0].strip()
            user_input = user_input.split("=")[1].strip()
        res = solve(user_input)
        if res and left_val:
            if res not in ["Division by zero", "Nothing was input"]:
                variable_dict[left_val] = res
            else:
                return res
            return
        elif res:
            return res
        return
    else:
        if user_input == "/exit":
            return "Bye!"
        if user_input == "/help":
            return "The program calculates the sum, subtraction, multiplication and/or division of numbers" \
                   "and also stores calculations in variables."
        return "Unknown command"


def main():
    while True:
        result = calculator()
        if result:
            print(result)
            if result == "Bye!":
                break


if __name__ == "__main__":
    main()