"""ASTx Python transpiler."""

from typing import Type

from plum import dispatch

import astx


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
    def visit(self, node: Type[astx.Int32]) -> str:
        """Handle Int32 nodes."""
        return "int"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralBoolean) -> str:
        """Handle LiteralBoolean nodes."""
        return "True" if node.value else "False"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralInt32) -> str:
        """Handle LiteralInt32 nodes."""
        return str(node.value)

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

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.UnaryOp) -> str:
        """Handle UnaryOp nodes."""
        operand = self.visit(node.operand)
        return f"({node.op_code}{operand})"

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
    def visit(self, node: Type[astx.Complex32]) -> str:
        """Handle Complex32 nodes."""
        return "(float, float)"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: Type[astx.Complex64]) -> str:
        """Handle Complex64 nodes."""
        return "(float, float)"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex32) -> str:
        """Handle LiteralComplex32 nodes."""
        real = node.value.real
        imag = node.value.imag
        return f"({real}, {imag})"

    @dispatch  # type: ignore[no-redef]
    def visit(self, node: astx.LiteralComplex64) -> str:
        """Handle LiteralComplex64 nodes."""
        real = node.value.real
        imag = node.value.imag
        return f"({real}, {imag})"
