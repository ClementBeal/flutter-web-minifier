from app.minifier import minify


def test_literal__convert_boolean_string__simple_true():
    program = "true"

    assert minify(program) == "!0"


def test_literal__convert_boolean_string__simple_false():
    program = "false"

    assert minify(program) == "!1"


def test_literal__convert_boolean_string__complex_true():
    program = "var a = true"

    assert minify(program) == "var a=!0"


def test_literal__convert_boolean_string__complex_false():
    program = "var a = false"

    assert minify(program) == "var a=!1"


def test_literal__use_fraction():
    program = "0.0125"

    assert minify(program) == "1/80"


def test_literal__use_fraction__with_variable():
    program = "var a = 0.0125"

    assert minify(program) == "var a=1/80"


def test_literal__use_scientific_notation__smaller_than_one():
    program = "0.00001"

    assert minify(program) == "1e-5"


def test_literal__use_pi_constant():
    program = "var a=3.141592653589793"

    assert minify(program) == "var a=Math.PI"


def test_literal__use_scientific_notation__greater_than_one():
    program = "10000"

    assert minify(program) == "1e4"


def test_literal__use_scientific_notation__does_nothing():
    program = "100"

    assert minify(program) == "100"
