"""ASTx Python transpiler."""

from typing import Type

from plum import dispatch
from typeguard import typechecked

import astx


@typechecked
class ASTxPythonTranspiler:
    """
    Transpiler that converts ASTx nodes to Python code.

    Notes
    -----
    Please keep the visit method in alphabet order according to the node type.
    The visit method for astx.AST should be the first one.
    """

    def __init__(self) -> None:
        self.indent_level = 0
        self.indent_str = "    "  # 4 spaces

    def _generate_block(self, block: astx.Block) -> str:
        """Generate code for a block of statements with proper indentation."""
        self.indent_level += 1
        indent = self.indent_str * self.indent_level
        lines = [indent + self.visit(node) for node in block.nodes]
        result = (
            "\n".join(lines)
            if lines
            else self.indent_str * self.indent_level + "pass"
        )
        self.indent_level -= 1
        return result

    @dispatch.abstract
    def visit(self, expr: astx.AST) -> str:
        """Translate an ASTx expression."""
        raise Exception(f"Not implemented yet ({expr}).")

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.AliasExpr) -> str:
        """Handle AliasExpr nodes."""
        if node.asname:
            return f"{node.name} as {node.asname}"
        return f"{node.name}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Argument) -> str:
        """Handle UnaryOp nodes."""
        type_ = self.visit(node.type_)
        return f"{node.name}: {type_}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Arguments) -> str:
        """Handle UnaryOp nodes."""
        return ", ".join([self.visit(arg) for arg in node.nodes])

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.BinaryOp) -> str:
        """Handle BinaryOp nodes."""
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        return f"({lhs} {node.op_code} {rhs})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Block) -> str:
        """Handle Block nodes."""
        return self._generate_block(node)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ForRangeLoopExpr) -> str:
        """Handle ForRangeLoopExpr nodes."""
        return (
            f"result = [{self.visit(node.body)} for "
            f" {node.variable.name} in range "
            f"({self.visit(node.start)},{self.visit(node.end)},"
            f"{self.visit(node.step)})]"
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Function) -> str:
        """Handle Function nodes."""
        args = self.visit(node.prototype.args)
        returns = (
            f" -> {self.visit(node.prototype.return_type)}"
            if node.prototype.return_type
            else ""
        )
        header = f"def {node.name}({args}){returns}:"
        body = self.visit(node.body)
        return f"{header}\n{body}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.FunctionReturn) -> str:
        """Handle FunctionReturn nodes."""
        value = self.visit(node.value) if node.value else ""
        return f"return {value}"

    def visit(self, node: astx.IfExpr) -> str:
        """Handle IfExpr nodes."""
        if node.else_:
            return (
                f"{self.visit(node.then)} if "
                f" {self.visit(node.condition)}"
                f" else {self.visit(node.else_)}"
            )
        return f"{self.visit(node.then)} if " f" {self.visit(node.condition)}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.IfStmt) -> str:
        """Handle IfStmt nodes."""
        if node.else_:
            return (
                f"if {self.visit(node.condition)}:"
                f"\n{self._generate_block(node.then)}"
                f"\nelse:"
                f"\n{self._generate_block(node.else_)}"
            )
        return (
            f"if {self.visit(node.condition)}:"
            f"\n{self._generate_block(node.then)}"
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> str:
        """Handle ImportFromStmt nodes."""
        names = [self.visit(name) for name in node.names]
        level_dots = "." * node.level
        module_str = (
            f"{level_dots}{node.module}" if node.module else level_dots
        )
        names_str = ", ".join(str(name) for name in names)
        return f"from {module_str} import {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportExpr) -> str:
        """Handle ImportExpr nodes."""
        names = [self.visit(name) for name in node.names]
        names_list = []
        for name in names:
            str_ = f"__import__('{name}') "
            names_list.append(str_)
        names_str = ", ".join(x for x in names_list)

        # name if one import or name1, name2, etc if multiple imports
        num = [
            "" if len(names) == 1 else str(n) for n in range(1, len(names) + 1)
        ]
        call = ["module" + str(n) for n in num]
        call_str = ", ".join(x for x in call)

        # assign tuple if multiple imports
        names_str = (
            names_str if len(names_list) == 1 else "(" + names_str + ")"
        )

        return f"{call_str} = {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromExpr) -> str:
        """Handle ImportFromExpr nodes."""
        names = [self.visit(name) for name in node.names]
        level_dots = "." * node.level
        module_str = (
            f"{level_dots}{node.module}" if node.module else level_dots
        )
        names_list = []
        for name in names:
            str_ = (
                f"getattr(__import__('{module_str}', "
                f"fromlist=['{name}']), '{name}')"
            )
            names_list.append(str_)
        names_str = ", ".join(x for x in names_list)

        # name if one import or name1, name2, etc if multiple imports
        num = [
            "" if len(names) == 1 else str(n) for n in range(1, len(names) + 1)
        ]
        call = ["name" + str(n) for n in num]
        call_str = ", ".join(x for x in call)

        # assign tuple if multiple imports
        names_str = (
            names_str if len(names_list) == 1 else "(" + names_str + ")"
        )

        return f"{call_str} = {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportStmt) -> str:
        """Handle ImportStmt nodes."""
        names = [self.visit(name) for name in node.names]
        names_str = ", ".join(x for x in names)
        return f"import {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.ImportFromStmt) -> str:
        """Handle ImportFromStmt nodes."""
        names = [self.visit(name) for name in node.names]
        level_dots = "." * node.level
        module_str = (
            f"{level_dots}{node.module}" if node.module else level_dots
        )
        names_str = ", ".join(str(name) for name in names)
        return f"from {module_str} import {names_str}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LambdaExpr) -> str:
        """Handle LambdaExpr nodes."""
        params_str = ", ".join(param.name for param in node.params)
        return f"lambda {params_str}: {self.visit(node.body)}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> str:
        """Handle LiteralBoolean nodes."""
        return "True" if node.value else "False"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex32) -> str:
        """Handle LiteralComplex32 nodes."""
        real = node.value.real
        imag = node.value.imag
        return f"complex({real}, {imag})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex64) -> str:
        """Handle LiteralComplex64 nodes."""
        real = node.value.real
        imag = node.value.imag
        return f"complex({real}, {imag})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat16) -> str:
        """Handle LiteralFloat nodes."""
        return str(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat32) -> str:
        """Handle LiteralFloat nodes."""
        return str(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralFloat64) -> str:
        """Handle LiteralFloat nodes."""
        return str(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> str:
        """Handle LiteralInt32 nodes."""
        return str(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8String) -> str:
        """Handle LiteralUTF8String nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralUTF8Char) -> str:
        """Handle LiteralUTF8Char nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Type[astx.Complex32]) -> str:
        """Handle Complex32 nodes."""
        return "Complex"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Type[astx.Complex64]) -> str:
        """Handle Complex64 nodes."""
        return "Complex"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Type[astx.Float16]) -> str:
        """Handle Float nodes."""
        return "float"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Type[astx.Float32]) -> str:
        """Handle Float nodes."""
        return "float"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Type[astx.Float64]) -> str:
        """Handle Float nodes."""
        return "float"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Type[astx.Int32]) -> str:
        """Handle Int32 nodes."""
        return "int"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.TypeCastExpr) -> str:
        """Handle TypeCastExpr nodes."""
        return (
            f"cast({self.visit(node.target_type.__class__)}, {node.expr.name})"
        )

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> str:
        """Handle UnaryOp nodes."""
        operand = self.visit(node.operand)
        return f"({node.op_code}{operand})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UTF8Char) -> str:
        """Handle UTF8Char nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UTF8String) -> str:
        """Handle UTF8String nodes."""
        return repr(node.value)

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.Variable) -> str:
        """Handle Variable nodes."""
        return node.name

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.VariableAssignment) -> str:
        """Handle VariableAssignment nodes."""
        target = node.name
        value = self.visit(node.value)
        return f"{target} = {value}"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileExpr) -> str:
        """Handle WhileExpr nodes."""
        condition = self.visit(node.condition)
        body = self.visit(node.body)
        return f"[{body} for _ in iter(lambda: {condition}, False)]"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.WhileStmt) -> str:
        """Handle WhileStmt nodes."""
        condition = self.visit(node.condition)
        body = self._generate_block(node.body)
        return f"while {condition}:\n{body}"
