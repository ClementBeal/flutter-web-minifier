from fractions import Fraction
import math
import traceback
import esprima

from .cache import clean_tree


def minify(data: str) -> str:
    a = esprima.parseScript(data)

    a = clean_tree(a)

    def shorten_consequitive_duplicates(buffer: list[str]) -> list[str]:
        def get_array_generator(value, length):
            return f"...Array({length}).fill({value})"

        if len(buffer) > 2:
            new_buffer = []

            i = 1
            selected_value = buffer[0]
            counter = 1
            while i < len(buffer):
                if buffer[i] == selected_value:
                    counter += 1
                else:
                    possible_new_value = get_array_generator(selected_value, counter)

                    if len(",".join([selected_value] * counter)) > len(
                        possible_new_value
                    ):
                        new_buffer.append(possible_new_value)
                    else:
                        new_buffer.extend([selected_value] * counter)

                    counter = 1
                    selected_value = buffer[i]
                i += 1

            possible_new_value = get_array_generator(selected_value, counter)

            if len(",".join([selected_value] * counter)) > len(possible_new_value):
                new_buffer.append(possible_new_value)
            else:
                new_buffer.extend([selected_value] * counter)

            buffer = new_buffer

        return buffer

    def flatten_literal(data):
        if data.raw == "true":
            return "!0"
        elif data.raw == "false":
            return "!1"
        elif data.raw == "3.141592653589793":
            return "Math.PI"
        # elif isinstance(data.value, int):
        #     number = data.value
        #     power = math.log10(number)

        #     if power.is_integer():
        #         formated_number = "1e" + str(int(power))
        #         if (len(formated_number)) < len(str(number)):
        #             return formated_number
        elif isinstance(data.value, float):
            number = data.value
            power = math.log10(number)

            if power.is_integer():
                formated_number = "1e" + str(int(power))
                if (len(formated_number)) < len(str(number)):
                    return formated_number

            f = Fraction(data.value).limit_denominator()

            fraction_str = f"{f.numerator}/{f.denominator}"
            if len(fraction_str) < len(data.raw):
                return f"{f.numerator}/{f.denominator}"

        return data.raw

    def flatten_array_expression(data):
        buffer = []
        for element in data.elements:
            buffer.append(flatten_js(element))

        return "[" + ",".join(shorten_consequitive_duplicates(buffer)) + "]"

    def flatten_binary_expression(data):
        operator = data.operator
        if operator == "in" or operator == "instanceof":
            return flatten_js(data.left) + " " + operator + " " + flatten_js(data.right)

        # if data.right.type == "UnaryExpression" and data.right.operator == "-":
        #     if operator == "-":
        #         operator = "+"
        #     data.right = data.right.argument

        return flatten_js(data.left) + operator + flatten_js(data.right)

    def flatten_identifier(data):
        return data.name

    def flatten_variable_declarator(declaration):
        if declaration.init:
            return declaration.id.name + "=" + flatten_js(declaration.init)

        return declaration.id.name

    def flatten_variable_declaration(data):
        buffer = []
        for declaration in data.declarations:
            buffer.append(flatten_js(declaration))

        return data.kind + " " + ",".join(buffer)

    def flatten_block_statement(data):
        output = "{"

        buffer = []
        for element in data.body:
            buffer.append(flatten_js(element))

        output += "\n".join(buffer)
        output += "}"

        return output

    def flatten_function(data):
        function_name = data.id.name
        output = (
            f"async function {function_name}("
            if data.isAsync
            else f"function {function_name}("
        )

        params = []
        for param in data.params:
            params.append(flatten_js(param))

        if len(params):
            output += ",".join(params)

        output += ")" + flatten_js(data.body)

        return output

    def flatten_call_expression(script):
        # return (
        #     "("
        #     + flatten_js(script.callee)
        #     + ")"
        #     + "("
        #     + ",".join([flatten_js(arg) for arg in script.arguments])
        #     + ")"
        # )
        return (
            flatten_js(script.callee)
            + "("
            + ",".join([flatten_js(arg) for arg in script.arguments])
            + ")"
        )

    def flatten_expression_statement(script):
        # return "(" + flatten_js(script.expression) + ")"
        return flatten_js(script.expression)

    def flatten_function_expression(script):
        name = flatten_js(script.id) if script.id else ""
        output = f"async function {name}(" if script.isAsync else f"function {name}("

        params = []
        for param in script.params:
            params.append(flatten_js(param))

        if len(params):
            output += ",".join(params)

        output += ")" + flatten_js(script.body)

        return output

    def flatten_for_statement(script):
        output = "for("

        buffer = ["", "", ""]

        if script.init:
            buffer[0] = flatten_js(script.init)
        if script.test:
            buffer[1] = flatten_js(script.test)
        if script.update:
            buffer[2] = flatten_js(script.update)

        output += ";".join(buffer) + ")" + flatten_js(script.body)

        return output

    def flatten_update_expression(script):
        arg = flatten_js(script.argument)

        return script.operator + arg if script.prefix else arg + script.operator

    def flatten_member_expression(script):
        if not script.computed:
            return flatten_js(script.object) + "." + flatten_js(script.property)
        else:
            return flatten_js(script.object) + "[" + flatten_js(script.property) + "]"

    def flatten_unary_expression(script):
        arg = flatten_js(script.argument)

        if script.prefix:
            if script.operator in ["typeof", "void", "delete"]:
                return script.operator + " " + arg
            return script.operator + arg
        else:
            return arg + script.operator

    def flatten_if_statement(script):
        # if we have something like `if(p==null)p=0`
        # we could do `p??=0` and save at least 9 chars every time
        if (
            script.test.type == "BinaryExpression"
            and script.consequent.type == "ExpressionStatement"
            and script.consequent.expression.type == "AssignmentExpression"
        ):
            variable_name_condition = script.test.left.name
            assignment_name_condition = script.consequent.expression.left.name

            if (
                variable_name_condition == assignment_name_condition
                and script.test.operator == "=="
                and script.test.left.value is None
            ):
                current_value = script.consequent.expression.right.raw
                value = (
                    "null"
                    if current_value is None or current_value == "None"
                    else script.consequent.expression.right.raw
                )
                return f"{variable_name_condition}??={script.consequent.expression.right.raw}"

        if_output = (
            "if(" + flatten_js(script.test) + ")" + flatten_js(script.consequent)
        )

        if script.alternate:
            return if_output + "\nelse " + flatten_js(script.alternate)
        return "if(" + flatten_js(script.test) + ")" + flatten_js(script.consequent)

    def flatten_new_expression(script):
        callee = flatten_js(script.callee)

        if len(script.arguments) == 0:
            return f"new {callee}"

        buffer = [flatten_js(arg) for arg in script.arguments]
        args = shorten_consequitive_duplicates(buffer)

        args = ",".join(args)

        return f"new {callee}({args})"

    def flatten_return_statement(script):
        if script.argument:
            return "return " + flatten_js(script.argument)
        return "return"

    def flatten_throw_statement(script):
        return "throw " + flatten_js(script.argument)

    def flatten_break_statement(script):
        return "break;"

    def flatten_assignment_expression(script):
        return flatten_js(script.left) + script.operator + flatten_js(script.right)

    def flatten_labeled_statement(script):
        return flatten_js(script.label) + ":" + flatten_js(script.body)

    def flatten_empty_statement(script):
        return ";"

    def flatten_switch_case(script):
        if script.test:
            output = "case " + flatten_js(script.test) + ":"
        else:
            output = "default:"
        output += "\n".join(
            [flatten_js(consequent) for consequent in script.consequent]
        )

        if len(script.consequent) == 1:
            output += "\n"

        return output

    def flatten_switch_statement(script):
        output = "switch (" + flatten_js(script.discriminant) + "){"

        cases = "\n".join([flatten_js(case) for case in script.cases])

        return output + cases + "}"

    def flatten_conditional_expression(script):
        return f"{flatten_js(script.test)}?{flatten_js(script.consequent)}:{flatten_js(script.alternate)}"

    def flatten_this_expression(script):
        return "this"

    def flatten_logical_expression(script):
        return (
            f"({flatten_js(script.left)}){script.operator}({flatten_js(script.right)})"
        )

    def flatten_object_expression(script):
        output = []

        for property in script.properties:
            output.append(flatten_js(property.key) + ":" + flatten_js(property.value))

        return "{" + ",".join(output) + "}"

    def flatten_try_statement(script):
        output = "try" + flatten_js(script.block)

        if script.handler:
            catch = flatten_js(script.handler)
            output += catch

        if script.finalizer:
            output += "finally" + flatten_js(script.finalizer)

        return output

    def flatten_catch_clause(script):
        return f"catch({flatten_js(script.param)}){flatten_js(script.body)}"

    def flatten_while_statement(script):
        return f"while({flatten_js(script.test)}){flatten_js(script.body)}"

    def flatten_sequence_statement(script):
        buffer = [flatten_js(expression) for expression in script.expressions]

        return ",".join(shorten_consequitive_duplicates(buffer))

    def flatten_do_while_statement(script):
        return f"do {{{flatten_js(script.body)}}} while ({flatten_js(script.test)})"

    def flatten_continue_statement(script):
        return "continue"

    def flatten_arrow_function_expression(script):
        output = "("
        params = []
        for param in script.params:
            params.append(flatten_js(param))

        if len(params):
            output += ",".join(params)
        output += ")=>"
        return f"{output}{flatten_js(script.body)}"

    def flatten_js(script):
        type = script.type

        try:
            if type == "Program":
                buffer = []
                for a in script.body:
                    buffer.append(flatten_js(a))
                return ";".join(buffer)
            elif type == "VariableDeclaration":
                return flatten_variable_declaration(script)
            elif type == "FunctionDeclaration":
                return flatten_function(script)
            elif type == "BlockStatement":
                return flatten_block_statement(script)
            elif type == "Identifier":
                return flatten_identifier(script)
            elif type == "BinaryExpression":
                return flatten_binary_expression(script)
            elif type == "Literal":
                return flatten_literal(script)
            elif type == "CallExpression":
                return flatten_call_expression(script)
            elif type == "ExpressionStatement":
                return flatten_expression_statement(script)
            elif type == "FunctionExpression":
                return flatten_function_expression(script)
            elif type == "ForStatement":
                return flatten_for_statement(script)
            elif type == "UpdateExpression":
                return flatten_update_expression(script)
            elif type == "VariableDeclarator":
                return flatten_variable_declarator(script)
            elif type == "ArrayExpression":
                return flatten_array_expression(script)
            elif type == "MemberExpression":
                return flatten_member_expression(script)
            elif type == "UnaryExpression":
                return flatten_unary_expression(script)
            elif type == "IfStatement":
                return flatten_if_statement(script)
            elif type == "NewExpression":
                return flatten_new_expression(script)
            elif type == "ReturnStatement":
                return flatten_return_statement(script)
            elif type == "ThrowStatement":
                return flatten_throw_statement(script)
            elif type == "SwitchStatement":
                return flatten_switch_statement(script)
            elif type == "SwitchCase":
                return flatten_switch_case(script)
            elif type == "LabeledStatement":
                return flatten_labeled_statement(script)
            elif type == "AssignmentExpression":
                return flatten_assignment_expression(script)
            elif type == "BreakStatement":
                return flatten_break_statement(script)
            elif type == "ConditionalExpression":
                return flatten_conditional_expression(script)
            elif type == "ThisExpression":
                return flatten_this_expression(script)
            elif type == "LogicalExpression":
                return flatten_logical_expression(script)
            elif type == "ObjectExpression":
                return flatten_object_expression(script)
            elif type == "TryStatement":
                return flatten_try_statement(script)
            elif type == "CatchClause":
                return flatten_catch_clause(script)
            elif type == "WhileStatement":
                return flatten_while_statement(script)
            elif type == "SequenceExpression":
                return flatten_sequence_statement(script)
            elif type == "DoWhileStatement":
                return flatten_do_while_statement(script)
            elif type == "ContinueStatement":
                return flatten_continue_statement(script)
            elif type == "ArrowFunctionExpression":
                return flatten_arrow_function_expression(script)
            elif type == "EmptyStatement":
                return flatten_empty_statement(script)
        except Exception as ex:
            traceback.print_stack()
            with open("log.json", "w") as a:
                a.write(str(script))
            exit(0)

    return flatten_js(a)
