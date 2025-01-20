"""ASTx collection types module."""

from __future__ import annotations

from typing import List

from public import public

from astx.base import AST, DataType
from astx.tools.typing import typechecked


@public
@typechecked
class CollectionType(DataType):
    """Base class for collection types."""

    pass


@public
@typechecked
class ListType(CollectionType):
    """Type representation of a list of elements of specific types."""

    def __init__(self, element_types: List[AST]) -> None:
        super().__init__()
        self.element_types = (
            element_types  # Ensure this attribute is correctly defined
        )

    def __str__(self) -> str:
        """Return a structural representation of the list type."""
        if not self.element_types:
            element_types_str = "AnyType"
        else:
            element_types_str = ", ".join(str(t) for t in self.element_types)
        return f"ListType[{element_types_str}]"

    def __repr__(self) -> str:
        """Return a string representation of the list type."""
        return self.__str__()


@public
@typechecked
class SetType(CollectionType):
    """Type representation of a set of elements of a specific type."""

    def __init__(self, element_type: AST) -> None:
        super().__init__()
        self.element_type = element_type

    def __str__(self) -> str:
        """Return a Structural representation of the set type."""
        return f"SetType[{self.element_type}]"

    def __repr__(self) -> str:
        """Return a string representation of the set type."""
        return self.__str__()


@public
@typechecked
class MapType(CollectionType):
    """Type representation of a map/dictionary."""

    def __init__(self, key_type: AST, value_type: AST) -> None:
        super().__init__()
        self.key_type = key_type
        self.value_type = value_type

    def __str__(self) -> str:
        """Return a structural representation of the map type."""
        return f"MapType[{self.key_type}, {self.value_type}]"

    def __repr__(self) -> str:
        """Return a string representation of the map type."""
        return self.__str__()


@public
@typechecked
class TupleType(CollectionType):
    """Type representation of a tuple of elements of specific types."""

    def __init__(self, element_types: List[AST]) -> None:
        super().__init__()
        self.element_types = element_types

    def __str__(self) -> str:
        """Return a string representation of the tuple."""
        types_str = ", ".join(str(t) for t in self.element_types)
        return f"TupleType[{types_str}]"

    def __repr__(self) -> str:
        """Return a string representation of the tuple."""
        return self.__str__()
