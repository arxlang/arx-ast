"""Test Python Transpiler."""

from typing import Dict, List, Set

import astx

from astx.literals.base import Literal
from astx.tools.transpilers import python as astx2py

transpiler = astx2py.ASTxPythonTranspiler()


def test_transpiler_multiple_imports_stmt() -> None:
    """Test astx.ImportStmt multiple imports."""
    alias1 = astx.AliasExpr(name="math")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")

    # Create an import statement
    import_stmt = astx.ImportStmt(names=[alias1, alias2])

    # Generate Python code
    generated_code = transpiler.visit(import_stmt)

    expected_code = "import math, matplotlib as mtlb"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_import_from_stmt() -> None:
    """Test astx.ImportFromStmt importing from module."""
    alias = astx.AliasExpr(name="pyplot", asname="plt")

    import_from_stmt = astx.ImportFromStmt(
        module="matplotlib", names=[alias], level=0
    )

    # Generate Python code
    generated_code = transpiler.visit(import_from_stmt)

    expected_code = "from matplotlib import pyplot as plt"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_wildcard_import_from_stmt() -> None:
    """Test astx.ImportFromStmt wildcard import from module."""
    alias = astx.AliasExpr(name="*")

    import_from_stmt = astx.ImportFromStmt(module="matplotlib", names=[alias])

    # Generate Python code
    generated_code = transpiler.visit(import_from_stmt)

    expected_code = "from matplotlib import *"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_future_import_from_stmt() -> None:
    """Test astx.ImportFromStmt from future import."""
    alias = astx.AliasExpr(name="division")

    import_from_stmt = astx.ImportFromStmt(module="__future__", names=[alias])

    # Generate Python code
    generated_code = transpiler.visit(import_from_stmt)

    expected_code = "from __future__ import division"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_multiple_imports_expr() -> None:
    """Test astx.ImportExpr multiple imports."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")
    alias2 = astx.AliasExpr(name="pi")

    import_expr = astx.ImportExpr([alias1, alias2])

    # Generate Python code
    generated_code = transpiler.visit(import_expr)

    expected_code = (
        "module1, module2 = "
        "(__import__('sqrt as square_root') , "
        "__import__('pi') )"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_import_from_expr() -> None:
    """Test astx.ImportFromExpr importing from module."""
    alias1 = astx.AliasExpr(name="sqrt", asname="square_root")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Generate Python code
    generated_code = transpiler.visit(import_from_expr)

    expected_code = (
        "name = "
        "getattr(__import__('math', "
        "fromlist=['sqrt as square_root']), "
        "'sqrt as square_root')"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_wildcard_import_from_expr() -> None:
    """Test astx.ImportFromExpr wildcard import from module."""
    alias1 = astx.AliasExpr(name="*")

    import_from_expr = astx.ImportFromExpr(module="math", names=[alias1])

    # Generate Python code
    generated_code = transpiler.visit(import_from_expr)

    expected_code = "name = getattr(__import__('math', fromlist=['*']), '*')"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_future_import_from_expr() -> None:
    """Test astx.ImportFromExpr from future import."""
    alias1 = astx.AliasExpr(name="division")

    import_from_expr = astx.ImportFromExpr(module="__future__", names=[alias1])

    # Generate Python code
    generated_code = transpiler.visit(import_from_expr)

    expected_code = (
        "name = "
        "getattr(__import__('__future__', "
        "fromlist=['division']), "
        "'division')"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_relative_import_from_expr() -> None:
    """Test astx.ImportFromExpr relative imports."""
    alias1 = astx.AliasExpr(name="division")
    alias2 = astx.AliasExpr(name="matplotlib", asname="mtlb")

    import_from_expr = astx.ImportFromExpr(names=[alias1, alias2], level=1)

    # Generate Python code
    generated_code = transpiler.visit(import_from_expr)

    expected_code = (
        "name1, name2 = "
        "(getattr("
        "__import__('.', fromlist=['division']), "
        "'division'), "
        "getattr("
        "__import__('.', fromlist=['matplotlib as mtlb']), "
        "'matplotlib as mtlb'))"
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_lambdaexpr() -> None:
    """Test astx.LambdaExpr."""
    params = astx.Arguments(astx.Argument(name="x", type_=astx.Int32()))
    body = astx.BinaryOp(
        op_code="+", lhs=astx.Variable(name="x"), rhs=astx.LiteralInt32(1)
    )

    lambda_expr = astx.LambdaExpr(params=params, body=body)

    # Generate Python code
    generated_code = transpiler.visit(lambda_expr)

    expected_code = "lambda x: (x + 1)"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_lambdaexpr_noparams() -> None:
    """Test astx.LambdaExpr without params."""
    body = astx.LiteralInt32(1)

    lambda_expr = astx.LambdaExpr(body=body)

    # Generate Python code
    generated_code = transpiler.visit(lambda_expr)

    expected_code = "lambda : 1"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_transpiler_function() -> None:
    """Test astx.Function."""
    # Function parameters
    args = astx.Arguments(
        astx.Argument(name="x", type_=astx.Int32()),
        astx.Argument(name="y", type_=astx.Int32()),
    )

    # Function body
    body = astx.Block()
    body.append(
        astx.VariableAssignment(
            name="result",
            value=astx.BinaryOp(
                op_code="+",
                lhs=astx.Variable(name="x"),
                rhs=astx.Variable(name="y"),
                loc=astx.SourceLocation(line=2, col=8),
            ),
            loc=astx.SourceLocation(line=2, col=4),
        )
    )
    body.append(
        astx.FunctionReturn(
            value=astx.Variable(name="result"),
            loc=astx.SourceLocation(line=3, col=4),
        )
    )

    # Function definition
    add_function = astx.Function(
        prototype=astx.FunctionPrototype(
            name="add",
            args=args,
            return_type=astx.Int32(),
        ),
        body=body,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Generate Python code
    generated_code = transpiler.visit(add_function)
    expected_code = "\n".join(
        [
            "def add(x: int, y: int) -> int:",
            "    result = (x + y)",
            "    return result",
        ]
    )

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_int32() -> None:
    """Test astx.LiteralInt32."""
    # Create a LiteralInt32 node
    literal_int32_node = astx.LiteralInt32(value=42)

    # Generate Python code
    generated_code = transpiler.visit(literal_int32_node)
    expected_code = "42"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float16() -> None:
    """Test astx.LiteralFloat16."""
    # Create a LiteralFloat16 node
    literal_float16_node = astx.LiteralFloat16(value=3.14)

    # Generate Python code
    generated_code = transpiler.visit(literal_float16_node)
    expected_code = "3.14"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float32() -> None:
    """Test astx.LiteralFloat32."""
    # Create a LiteralFloat32 node
    literal_float32_node = astx.LiteralFloat32(value=2.718)

    # Generate Python code
    generated_code = transpiler.visit(literal_float32_node)
    expected_code = "2.718"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_float64() -> None:
    """Test astx.LiteralFloat64."""
    # Create a LiteralFloat64 node
    literal_float64_node = astx.LiteralFloat64(value=1.414)

    # Generate Python code
    generated_code = transpiler.visit(literal_float64_node)
    expected_code = "1.414"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_complex32() -> None:
    """Test astx.LiteralComplex32."""
    # Create a LiteralComplex32 node
    literal_complex32_node = astx.LiteralComplex32(real=1, imag=2.8)

    # Generate Python code
    generated_code = transpiler.visit(literal_complex32_node)
    expected_code = "complex(1, 2.8)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_literal_complex64() -> None:
    """Test astx.LiteralComplex64."""
    # Create a LiteralComplex64 node
    literal_complex64_node = astx.LiteralComplex64(real=3.5, imag=4)

    # Generate Python code
    generated_code = transpiler.visit(literal_complex64_node)
    expected_code = "complex(3.5, 4)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_typecastexpr() -> None:
    """Test astx.TypeCastExpr."""
    # Expression to cast
    expr = astx.Variable(name="x")
    # Target type for casting
    target_type = astx.Int32()
    # Create the TypeCastExpr
    cast_expr = astx.TypeCastExpr(expr=expr, target_type=target_type)

    generated_code = transpiler.visit(cast_expr)
    expected_code = "cast(int, x)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_utf8_char() -> None:
    """Test astx.Utf8Char."""
    # Create a Utf8Char node
    utf8_char_node = astx.LiteralUTF8Char(value="c")

    # Generate Python code
    generated_code = transpiler.visit(utf8_char_node)
    expected_code = repr("c")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_utf8_string() -> None:
    """Test astx.Utf8String."""
    # Create a Utf8String node
    utf8_string_node = astx.LiteralUTF8String(value="hello")

    # Generate Python code
    generated_code = transpiler.visit(utf8_string_node)
    expected_code = repr("hello")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_utf8_char() -> None:
    """Test astx.LiteralUtf8Char."""
    # Create a LiteralUtf8Char node
    literal_utf8_char_node = astx.LiteralUTF8Char(value="a")

    # Generate Python code
    generated_code = transpiler.visit(literal_utf8_char_node)
    expected_code = repr("a")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_utf8_string() -> None:
    """Test astx.LiteralUtf8String."""
    # Create a LiteralUtf8String node
    literal_utf8_string_node = astx.LiteralUTF8String(value="world")

    # Generate Python code
    generated_code = transpiler.visit(literal_utf8_string_node)
    expected_code = repr("world")

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_for_range_loop_expr() -> None:
    """Test `For Range Loop` expression`."""
    decl_a = astx.InlineVariableDeclaration(
        "a", type_=astx.Int32(), value=astx.LiteralInt32(-1)
    )
    start = astx.LiteralInt32(0)
    end = astx.LiteralInt32(10)
    step = astx.LiteralInt32(1)
    body = astx.Block()
    body.append(astx.LiteralInt32(2))
    for_expr = astx.ForRangeLoopExpr(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    generated_code = transpiler.visit(for_expr)
    expected_code = "result = [    2 for  a in range (0,10,1)]"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_binary_op() -> None:
    """Test astx.BinaryOp for addition operation."""
    # Create a BinaryOp node for the expression "x + y"
    lhs = astx.Variable(name="x")
    rhs = astx.Variable(name="y")
    binary_op = astx.BinaryOp(op_code="+", lhs=lhs, rhs=rhs)

    # Generate Python code
    generated_code = transpiler.visit(binary_op)

    # Expected code for the binary operation
    expected_code = "(x + y)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_while_stmt() -> None:
    """Test astx.WhileStmt."""
    # Define a condition: x < 5
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Define the loop body: x = x + 1
    update_expr = astx.VariableAssignment(
        name="x",
        value=astx.BinaryOp(
            op_code="+",
            lhs=x_var,
            rhs=astx.LiteralInt32(1),
            loc=astx.SourceLocation(line=2, col=4),
        ),
        loc=astx.SourceLocation(line=2, col=4),
    )

    # Create the body block
    body_block = astx.Block(name="while_body")
    body_block.append(update_expr)

    while_stmt = astx.WhileStmt(
        condition=condition,
        body=body_block,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Generate Python code
    generated_code = transpiler.visit(while_stmt)

    # Expected code for the WhileStmt
    expected_code = "while (x < 5):\n    x = (x + 1)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_ifexpr_with_else() -> None:
    """Test astx.IfExpr with else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # create then and else blocks
    then_block = astx.Block()
    else_block = astx.Block()

    # define literals
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)

    # define operations
    op1 = lit_2 + lit_3
    op2 = lit_2 - lit_3

    # Add statements to the then and else blocks
    then_block.append(op1)
    else_block.append(op2)

    # define if Expr
    if_expr = astx.IfExpr(condition=cond, then=then_block, else_=else_block)

    # Generate Python code
    generated_code = transpiler.visit(if_expr)

    # Expected code for the binary operation
    expected_code = "    (2 + 3) if  (1 > 2) else     (2 - 3)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_while_expr() -> None:
    """Test astx.WhileExpr."""
    # Define a condition: x < 5
    x_var = astx.Variable(name="x")
    condition = astx.BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=astx.LiteralInt32(5),
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Define the loop body: x = x + 1
    update_expr = astx.VariableAssignment(
        name="x",
        value=astx.BinaryOp(
            op_code="+",
            lhs=x_var,
            rhs=astx.LiteralInt32(1),
            loc=astx.SourceLocation(line=2, col=4),
        ),
        loc=astx.SourceLocation(line=2, col=4),
    )

    # Create the body block
    body_block = astx.Block(name="while_body")
    body_block.append(update_expr)

    while_stmt = astx.WhileExpr(
        condition=condition,
        body=body_block,
        loc=astx.SourceLocation(line=1, col=0),
    )

    # Generate Python code
    generated_code = transpiler.visit(while_stmt)

    # Expected code for the WhileExpr
    expected_code = "[    x = (x + 1) for _ in iter(lambda: (x < 5), False)]"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_ifexpr_without_else() -> None:
    """Test astx.IfExpr without else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # create then block
    then_block = astx.Block()

    # define literals
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)

    # define operation
    op1 = lit_2 + lit_3

    # Add statement to the then block
    then_block.append(op1)

    # define if Expr
    if_expr = astx.IfExpr(condition=cond, then=then_block)

    # Generate Python code
    generated_code = transpiler.visit(if_expr)

    # Expected code for the binary operation
    expected_code = "    (2 + 3) if  (1 > 2) else None"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_ifstmt_with_else() -> None:
    """Test astx.IfStmt with else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # create then and else blocks
    then_block = astx.Block()
    else_block = astx.Block()

    # define literals
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)

    # define operations
    op1 = lit_2 + lit_3
    op2 = lit_2 - lit_3

    # Add statements to the then and else blocks
    then_block.append(op1)
    else_block.append(op2)

    # define if Stmt
    if_stmt = astx.IfStmt(condition=cond, then=then_block, else_=else_block)

    # Generate Python code
    generated_code = transpiler.visit(if_stmt)

    # Expected code for the binary operation
    expected_code = "if (1 > 2):\n    (2 + 3)\nelse:\n    (2 - 3)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_ifstmt_without_else() -> None:
    """Test astx.IfStmt without else block."""
    # determine condition
    cond = astx.BinaryOp(
        op_code=">", lhs=astx.LiteralInt32(1), rhs=astx.LiteralInt32(2)
    )

    # create then block
    then_block = astx.Block()

    # define literals
    lit_2 = astx.LiteralInt32(2)
    lit_3 = astx.LiteralInt32(3)

    # define operation
    op1 = lit_2 + lit_3

    # Add statement to the then block
    then_block.append(op1)

    # define if Stmt
    if_stmt = astx.IfStmt(condition=cond, then=then_block)

    # Generate Python code
    generated_code = transpiler.visit(if_stmt)

    # Expected code for the binary operation
    expected_code = "if (1 > 2):\n    (2 + 3)"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_date_type() -> None:
    """Test Type[astx.Date]."""
    # Generate Python code for the type
    generated_code = transpiler.visit(astx.Date())
    expected_code = "date"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_time_type() -> None:
    """Test Type[astx.Time]."""
    # Generate Python code for the type
    generated_code = transpiler.visit(astx.Time())
    expected_code = "time"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_timestamp_type() -> None:
    """Test Type[astx.Timestamp]."""
    # Generate Python code for the type
    generated_code = transpiler.visit(astx.Timestamp())
    expected_code = "timestamp"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_datetime_type() -> None:
    """Test Type[astx.DateTime]."""
    # Generate Python code for the type
    generated_code = transpiler.visit(astx.DateTime())
    expected_code = "datetime"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_date() -> None:
    """Test astx.LiteralDate."""
    # Create a LiteralDate node
    literal_date_node = astx.LiteralDate(value="2024-11-24")

    # Generate Python code
    generated_code = transpiler.visit(literal_date_node)
    expected_code = "datetime.strptime('2024-11-24', '%Y-%m-%d').date()"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_time() -> None:
    """Test astx.LiteralTime."""
    # Create a LiteralTime node
    literal_time_node = astx.LiteralTime(value="14:30:00")

    # Generate Python code
    generated_code = transpiler.visit(literal_time_node)
    expected_code = "datetime.strptime('14:30:00', '%H:%M:%S').time()"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_timestamp() -> None:
    """Test astx.LiteralTimestamp."""
    # Create a LiteralTimestamp node
    literal_timestamp_node = astx.LiteralTimestamp(value="2024-11-24 14:30:00")

    # Generate Python code
    generated_code = transpiler.visit(literal_timestamp_node)
    expected_code = (
        "datetime.strptime('2024-11-24 14:30:00', '%Y-%m-%d %H:%M:%S')"
    )

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_literal_datetime() -> None:
    """Test astx.LiteralDateTime."""
    # Create a LiteralDateTime node
    literal_datetime_node = astx.LiteralDateTime(value="2024-11-24T14:30:00")

    # Generate Python code
    generated_code = transpiler.visit(literal_datetime_node)
    expected_code = (
        "datetime.strptime('2024-11-24T14:30:00', '%Y-%m-%dT%H:%M:%S')"
    )

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_transpiler_classdefstmt() -> None:
    """Test astx.ClassDefStmt."""
    # Create a class body
    class_body = astx.Block(name="MyClass_body")
    var1 = astx.Variable(name="var1")
    class_body.append(var1)

    # Create a class definition
    class_def = astx.ClassDefStmt(
        name="MyClass",
        body=class_body,
    )

    # Generate Python code
    generated_code = transpiler.visit(class_def)
    expected_code = "class MyClass:\n     var1"

    assert (
        generated_code == expected_code
    ), f"Expected '{expected_code}', but got '{generated_code}'"


def test_literal_list() -> None:
    """Test astx.LiteralList."""
    # Create a LiteralList node
    elements: List[Literal] = [
        astx.LiteralInt32(1),
        astx.LiteralInt32(2),
        astx.LiteralInt32(3),
    ]
    literal_list_node = astx.LiteralList(elements=elements)

    # Generate Python code
    generated_code = transpiler.visit(literal_list_node)
    expected_code = "[1, 2, 3]"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_set() -> None:
    """Test astx.LiteralSet."""
    # Create a LiteralSet node
    elements: Set[Literal] = {
        astx.LiteralInt32(1),
        astx.LiteralInt32(2),
        astx.LiteralInt32(3),
    }
    literal_set_node = astx.LiteralSet(elements=elements)

    # Generate Python code
    generated_code = transpiler.visit(literal_set_node)

    # Since sets are unordered, compare the evaluated sets
    generated_set = eval(generated_code)
    expected_set = {1, 2, 3}

    assert generated_set == expected_set, "generated_set != expected_set"


def test_literal_tuple() -> None:
    """Test astx.LiteralTuple."""
    # Create a LiteralTuple node
    elements = (
        astx.LiteralInt32(1),
        astx.LiteralInt32(2),
        astx.LiteralInt32(3),
    )
    literal_tuple_node = astx.LiteralTuple(elements=elements)

    # Generate Python code
    generated_code = transpiler.visit(literal_tuple_node)
    expected_code = "(1, 2, 3)"

    assert generated_code == expected_code, "generated_code != expected_code"


def test_literal_map() -> None:
    """Test astx.LiteralMap."""
    # Create a LiteralMap node
    elements: Dict[Literal, Literal] = {
        astx.LiteralInt32(1): astx.LiteralUTF8String("a"),
        astx.LiteralInt32(2): astx.LiteralUTF8String("b"),
    }
    literal_map_node = astx.LiteralMap(elements=elements)

    # Generate Python code
    generated_code = transpiler.visit(literal_map_node)

    # Compare the evaluated dictionaries
    generated_dict = eval(generated_code)
    expected_dict = {1: "a", 2: "b"}

    assert generated_dict == expected_dict, "generated_dict != expected_dict"
