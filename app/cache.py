from typing import Union
import esprima
from esprima.nodes import UnaryExpression, BinaryExpression, Literal


def is_number(a) -> bool:
    return isinstance(a, (int, float))


def is_number_node(a) -> bool:
    return (isinstance(a, Literal) and is_number(a.value)) or (
        isinstance(a, UnaryExpression) and is_number_node(a.argument)
    )


def get_number_from_node(a) -> Union[int, float]:
    if isinstance(a, Literal):
        return a.value
    if isinstance(a, UnaryExpression):
        operator = a.operator
        value = get_number_from_node(a.argument)
        if operator == "-":
            return -value
        else:
            return value

    raise Exception()


def unary_expression_eraser(o: UnaryExpression):
    """
    If the UnaryExpression is a prefix and its argument is a number
    Then report the operator to the literal
    ```js
    {
        type: "UnaryExpression",
        prefix: True,
        operator: "-",
        argument: {
            type: "Literal",
            value: 1,
            raw: "1"
        }
    }
    ```

    becomes
    ```js
    {
        type: "Literal",
        value: -1,
        raw: "-1"
    }
    ```
    """

    operator = o.operator

    if o.argument.type == "Literal":
        v = o.argument.value
        if isinstance(v, float) or isinstance(v, int):
            v = v * -1 if operator == "-" else v
            return Literal(v, str(v))

    return o


def binary_expression_reducer(o: BinaryExpression):
    operator = o.operator
    left = o.left
    right = o.right
    if is_number_node(left) and is_number_node(right):
        left_value = get_number_from_node(left)
        right_value = get_number_from_node(right)

        print(f"{operator} {left_value} {right_value}")
        if operator == "-":
            v = left_value - right_value
        elif operator == "+":
            v = left_value + right_value
        elif operator == "*":
            v = left_value * right_value
        elif operator == "/":
            if right_value == 0:
                return o
            v = left_value / right_value
        elif operator == "%":
            v = left_value % right_value

        if v < 0:
            return UnaryExpression(operator="-", argument=Literal(-v, str(-v)))
        return Literal(v, str(v))

    # elif not is_number_node(left) and is_number_node(right):

    return o


def clean_tree(a):
    string_variables = list()
    num_variables = list()
    function_calls = list()

    def parse_object(o):
        t = o.type

        # if t == "UnaryExpression":
        #     return unary_expression_eraser(o)
        if t == "BinaryExpression":
            o.left = parse_object(o.left)
            o.right = parse_object(o.right)
            return binary_expression_reducer(o)

        if t == "Literal":
            if isinstance(o.value, str):
                string_variables.append(o.value)
            if isinstance(o.value, float) or isinstance(o.value, int):
                num_variables.append(o.value)

        if t == "CallExpression":
            expression = o.callee

            if (
                expression.type == "MemberExpression"
                and expression.computed is False
                and expression.object.type == "Identifier"
                and expression.property.type == "Identifier"
            ):
                if (
                    len(expression.object.name) > 2
                    and len(expression.property.name) > 1
                ):
                    function_call = (
                        f"{expression.object.name}.{expression.property.name}"
                    )
                    function_calls.append(function_call)

                    # let's check if some Math.min/Math.max are nested
                    # Math.min(Math.min(2,3), 4)
                    # can be
                    # Math.min(2,3,4)
                    if function_call == "Math.min" or function_call == "Math.max":
                        i = 0
                        while i < len(o.arguments):
                            node = o.arguments[i]
                            if (
                                node.type == "CallExpression"
                                and node.callee.type == "MemberExpression"
                                and not node.callee.computed
                            ):
                                node_function_call = f"{node.callee.object.name}.{node.callee.property.name}"

                                # means we have Math.min == Math.min OR Math.max == Math.max
                                if function_call == node_function_call:
                                    o.arguments[i] = node.arguments[0]
                                    o.arguments.insert(i + 1, node.arguments[1])
                                    i += 1

                            i += 1

        for k, v in o.items():
            if isinstance(v, dict):
                setattr(o, k, parse_object(v))

            elif isinstance(v, list):
                setattr(o, k, parse_list(v))
            elif isinstance(v, esprima.nodes.Node):
                setattr(o, k, parse_object(v))
            # parse_object(getattr(o, key))
            # parse_object(o.key)

        return o

    def parse_list(o):
        for i, value in enumerate(o):
            if isinstance(value, dict):
                o[i] = parse_object(value)
            elif isinstance(value, list):
                o[i] = parse_list(value)
            elif isinstance(value, esprima.nodes.Node):
                o[i] = parse_object(value)

        return o

    a = parse_object(a)

    return a
