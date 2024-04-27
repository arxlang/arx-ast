"""Module for different kind of ASTx blocks."""

from __future__ import annotations

from typing import Optional, cast

from public import public

from astx.base import AST, ASTNodes, ReprStruct, SourceLocation


@public
class Block(ASTNodes):
    """The AST tree."""

    name: str
    position: int = 0

    def __init__(
        self,
        name: str = "entry",
        loc: SourceLocation = SourceLocation(0, 0),
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(loc=loc, parent=parent)
        self.name = name
        # note: maybe it would be nice to add options for rules, so
        #       it could have specific rules for the type of AST
        #       accepted
        self.nodes: list[AST] = []
        self.position: int = 0

    def append(self, value: AST) -> None:
        """Append a new node to the stack."""
        self.nodes.append(value)

    def __iter__(self) -> Block:
        """Overload `iter` magic function."""
        return self

    def __next__(self) -> AST:
        """Overload `next` magic function."""
        if self.position >= len(self.nodes):
            raise StopIteration()

        i = self.position
        self.position += 1
        return self.nodes[i]

    def get_struct(self, simplified: bool = True) -> ReprStruct:
        """Return the AST structure of the object."""
        block_node = []

        for node in self.nodes:
            block_node.append(node.get_struct(simplified))

        key = "BLOCK"
        value = cast(ReprStruct, block_node)

        return self._prepare_struct(key, value, simplified)
