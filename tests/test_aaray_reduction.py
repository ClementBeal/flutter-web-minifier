from app.minifier import minify


def test_array_reduction__all_elements_are_equal():
    program = "[null,null,null,null,null,null,null,null, 1]"

    assert minify(program) == "[...Array(8).fill(null),1]"


def test_array_reduction__2_reductions():
    program = "[null,null,null,null,null,null,null,null, 1, null,null,null,null,null,null,null,null, ]"

    assert minify(program) == "[...Array(8).fill(null),1,...Array(8).fill(null)]"


# def test_array_reduction__all_elements_are_equal():
#     program = "[null,null,null,null,null,null,null,null]"

#     assert minify(program) == "Array(8).fill(null)"
