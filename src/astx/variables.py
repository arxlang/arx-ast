from typing import List, Tuple

from astx.base import (
    DataType,
    ExprType,
    Expr,
    SourceLocation,
    ASTKind,
    StatementType,
)
from astx.blocks import Block
from astx.datatypes import DataTypeOps


class VarDecl(StatementType):
    """AST class for variable declaration."""

    var_names: List[Tuple[str, Expr]]
    type_name: str
    body: Block

    def __init__(
        self,
        var_names: List[Tuple[str, Expr]],
        type_name: str,
        body: Block,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the VarExprAST instance."""
        self.loc = loc
        self.var_names = var_names
        self.type_name = type_name
        self.body = body
        self.kind = ASTKind.VarKind


class Variable(DataTypeOps):
    """AST class for the variable usage."""

    type_: ExprType
    value: DataType

    def __init__(
        self,
        name: str,
        type_: ExprType,
        value: DataType,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc)
        self.name = name
        self.type_ = type_
        self.kind = ASTKind.VariableKind
        self.value: DataType = value
