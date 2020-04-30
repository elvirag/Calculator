import re
from collections import deque

variable_dict = {}


def str_to_num(a):
    a = float(a)
    if a.is_integer():
        return int(a)

    return a


def parse_input(input_line):
    elements = re.findall(r"([\-]*\w+|[-]+|[+]+|[*/^]|[()])", input_line)

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
            raise Exception("Invalid assignment")

        if variable not in variable_dict:
            raise Exception("Unknown variable")

        return variable_dict[variable]


def calculate_postfix(postfix):
    calculation_stack = deque()

    for element in postfix:
        if element in ["/", "*", "-", "+", "^"]:
            a = calculation_stack.pop()
            b = calculation_stack.pop()
            if element == "/":
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

    return str_to_num(calculation_stack[-1])


def is_operand(symbol):
    return symbol not in "+-/*^()"


def infix_to_postfix(symbols):
    postfix_stack = deque()
    postfix = []
    precedences = {'(': 0, "+": 1, '-': 1, '*': 2, '/': 2, '^': 3}

    for symbol in symbols:
        if is_operand(symbol):
            postfix.append(check_variable_valid_assignment(symbol))
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
        raise Exception("Invalid expression")

    return postfix


def solve(input_line):
    symbols = parse_input(input_line)
    postfix = infix_to_postfix(symbols)
    return calculate_postfix(postfix)


def validate_identifiers(input_line):
    m = re.search(r"\s*[A-Za-z]+[0-9]+|[0-9]+[A-Za-z]+\s*=", input_line)
    if m is not None:
        raise Exception("Invalid identifier")


def validate_expression(input_line):
    """This function handles not paired brackets, adjacent mul/dic signs and too many assignment symbols"""

    m = re.search(r"([*]{2,}|[/]{2,}|[\^]{2,})", input_line)
    paren = input_line.count("(") - input_line.count(")")
    if not (m is None and paren == 0):
        raise Exception("Invalid expression")
    if input_line.count("=") > 1:
        raise Exception("Invalid assignment")


def calculator():
    user_input = input()
    if user_input == "":
        return ""
    if not user_input.startswith("/"):
        validate_expression(user_input)
        validate_identifiers(user_input)

        left_val = None
        if "=" in user_input:
            left_val = user_input.split("=")[0].strip()
            user_input = user_input.split("=")[1].strip()
        result = solve(user_input)
        if left_val:
            variable_dict[left_val] = result
        else:
            return result
    else:
        if user_input == "/exit":
            return "Bye!"
        elif user_input == "/help":
            return "The program calculates the sum, subtraction, multiplication and/or division of numbers" \
                   "and also stores calculations in variables."
        else:
            raise Exception("Unknown command")


def main():
    while True:
        try:
            result = calculator()
            if result:
                print(result)
                if result == "Bye!":
                    break
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(e)


if __name__ == "__main__":
    main()
