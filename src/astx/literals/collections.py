"""ASTX literal representations of collection types."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple, Type

from public import public

from astx.base import AST, NO_SOURCE_LOCATION, SourceLocation
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.base import AnyType
from astx.types.collections import ListType, MapType, SetType, TupleType


@public
@typechecked
class LiteralList(Literal):
    """Literal representation of a list."""

    elements: List[Literal]

    def __init__(
        self,
        elements: List[Literal],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        super().__init__(loc)
        self.elements = elements

        # Collect the unique type classes from the elements
        type_classes: Set[Type[AST]] = {type(elem.type_) for elem in elements}

        # Create instances of these types
        element_types: List[AST] = [
            type_class() for type_class in type_classes
        ]

        # Sort the element types based on their string representation
        element_types.sort(key=lambda t: str(t))

        # Assign the type_ attribute to a ListType
        self.type_ = ListType(element_types)
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the literal list."""
        return f"LiteralList({self.elements})"

    def __repr__(self) -> str:
        """Return a string representation of the literal list."""
        return self.__str__()


@public
@typechecked
class LiteralSet(Literal):
    """Literal representation of a set."""

    elements: Set[Literal]

    def __init__(
        self,
        elements: Set[Literal],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        super().__init__(loc)
        self.elements = elements

        element_type_classes = {type(elem.type_) for elem in elements}

        if len(element_type_classes) == 1:
            element_type_class = element_type_classes.pop()
            element_type: AST = element_type_class()
        else:
            element_type = AnyType()

        self.type_ = SetType(element_type)
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the set."""
        return f"LiteralSet({self.elements})"

    def __repr__(self) -> str:
        """Return a structural representation of the set."""
        return self.__str__()


@public
@typechecked
class LiteralMap(Literal):
    """Literal representation of a map/dictionary."""

    elements: Dict[Literal, Literal]

    def __init__(
        self,
        elements: Dict[Literal, Literal],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        super().__init__(loc)
        self.elements = elements

        key_type_classes = {type(key.type_) for key in elements.keys()}
        value_type_classes = {type(value.type_) for value in elements.values()}

        if len(key_type_classes) == 1:
            key_type_class = key_type_classes.pop()
            key_type: AST = key_type_class()
        else:
            key_type = AnyType()

        if len(value_type_classes) == 1:
            value_type_class = value_type_classes.pop()
            value_type: AST = value_type_class()
        else:
            value_type = AnyType()

        self.type_ = MapType(key_type, value_type)
        self.loc = loc

    def __str__(self) -> str:
        """Represent the map as a string."""
        return f"LiteralMap({self.elements})"

    def __repr__(self) -> str:
        """Return a structural representation of the map."""
        return self.__str__()


@public
@typechecked
class LiteralTuple(Literal):
    """Literal representation of a tuple."""

    elements: Tuple[Literal, ...]

    def __init__(
        self,
        elements: Tuple[Literal, ...],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        super().__init__(loc)
        self.elements = elements

        element_type_classes = [type(elem.type_) for elem in elements]
        element_types: List[AST] = [
            type_class() for type_class in element_type_classes
        ]

        self.type_ = TupleType(element_types)
        self.loc = loc

    def __str__(self) -> str:
        """Represent the tuple as a string."""
        return f"LiteralTuple({self.elements})"

    def __repr__(self) -> str:
        """Return a structural representation of the tuple."""
        return self.__str__()
