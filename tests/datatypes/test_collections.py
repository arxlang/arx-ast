"""Tests for collection data types."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from astx.literals.base import Literal
from astx.literals.collections import (
    LiteralList,
    LiteralMap,
    LiteralSet,
    LiteralTuple,
)
from astx.literals.numeric import LiteralInt32
from astx.types.collections import ListType, MapType, SetType, TupleType
from astx.types.numeric import Int32
from astx.types.operators import BinaryOp, UnaryOp
from astx.variables import Variable

VAR_A = Variable("a")

COLLECTION_LITERAL_CLASSES = [
    LiteralList,
    LiteralSet,
    LiteralTuple,
    LiteralMap,
]


def test_literal_list_creation() -> None:
    """Test creation of LiteralList."""
    elements: List[Literal] = [
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    ]
    lit_list = LiteralList(elements)
    assert isinstance(lit_list, LiteralList)
    assert isinstance(lit_list.type_, ListType)
    element_types = lit_list.type_.element_types
    # After fixing deduplication, element_types should have length 1
    assert (
        len(element_types) == 1
    ), f"Expected 1 element type, got {len(element_types)}"
    # Check that the single element type is Int32
    assert isinstance(
        element_types[0], Int32
    ), f"Expected element type Int32, got {type(element_types[0])}"
    assert lit_list.elements == elements


def test_literal_list_binary_operation_addition() -> None:
    """Test binary addition of LiteralList."""
    elements1: List[Literal] = [LiteralInt32(1), LiteralInt32(2)]
    elements2: List[Literal] = [LiteralInt32(3), LiteralInt32(4)]
    lit_list1 = LiteralList(elements1)
    lit_list2 = LiteralList(elements2)
    combined = lit_list1 + lit_list2

    assert isinstance(combined, BinaryOp)
    assert combined.op_code == "+"
    assert combined.lhs == lit_list1
    assert combined.rhs == lit_list2


def test_literal_list_unary_operation_negation() -> None:
    """Test unary negation of LiteralList."""
    elements: List[Literal] = [
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    ]
    lit_list = LiteralList(elements)
    negated = -lit_list

    assert isinstance(negated, UnaryOp)
    assert negated.op_code == "-"
    assert negated.operand == lit_list


def test_literal_set_creation() -> None:
    """Test creation of LiteralSet."""
    elements: Set[Literal] = {
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    }
    lit_set = LiteralSet(elements)
    assert isinstance(lit_set, LiteralSet)
    assert isinstance(lit_set.type_, SetType)
    assert isinstance(lit_set.type_.element_type, Int32)
    assert lit_set.elements == elements


def test_literal_tuple_creation() -> None:
    """Test creation of LiteralTuple."""
    elements: Tuple[Literal, ...] = (
        LiteralInt32(1),
        LiteralInt32(2),
        LiteralInt32(3),
    )
    lit_tuple = LiteralTuple(elements)
    assert isinstance(lit_tuple, LiteralTuple)
    assert isinstance(lit_tuple.type_, TupleType)
    assert all(isinstance(t, Int32) for t in lit_tuple.type_.element_types)
    assert lit_tuple.elements == elements


def test_literal_map_creation() -> None:
    """Test creation of LiteralMap."""
    elements: Dict[Literal, Literal] = {
        LiteralInt32(1): LiteralInt32(10),
        LiteralInt32(2): LiteralInt32(20),
    }
    lit_map = LiteralMap(elements)
    assert isinstance(lit_map, LiteralMap)
    assert isinstance(lit_map.type_, MapType)
    assert isinstance(lit_map.type_.key_type, Int32)
    assert isinstance(lit_map.type_.value_type, Int32)
    assert lit_map.elements == elements
