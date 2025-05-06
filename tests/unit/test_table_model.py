import pytest

from cymple.table_model import TableModel, Field, Expr


# Dummy subclass for testing
class Location(TableModel):
    id: str
    name: str
    age: int


def test_class_field_access():
    assert Location.id == "id"
    assert Location.name == "name"
    assert Location.age == "age"


def test_instance_field_access_with_alias():
    loc = Location(alias="l")
    assert str(loc.id) == "l.id"
    assert str(loc.name) == "l.name"
    assert str(loc.age) == "l.age"


def test_expression_chaining():
    loc = Location("l")
    expr = (loc.id == "ABC") & (loc.age > 30) | (loc.name != "Test")
    assert str(expr) == '(((l.id = \'ABC\') AND (l.age > 30)) OR (l.name <> \'Test\'))'


def test_math_expressions():
    loc = Location("n")
    expr = (loc.age + 5) * 2 - 1 / (loc.name)
    assert str(expr) == '(((n.age + 5) * 2) - (1 / n.name))'


def test_field_repr_and_str():
    field = Field("age", int, "n")
    assert str(field) == "n.age"
    assert repr(field) == "n.age"


def test_expr_repr():
    expr = Expr("x", "+", 5)
    assert repr(expr) == "(x + 5)"


def test_class_repr():
    assert repr(Location) == "LOCATION"


def test_instance_repr_with_alias():
    loc = Location("x")
    assert repr(loc) == "x"


def test_instance_repr_without_alias():
    loc = Location()
    assert repr(loc) == "LOCATION"


def test_field_fallback_when_no_alias():
    field = Field("id", str)
    assert str(field) == "id"


def test_table_model_instantiation_sets_fields():
    m = Location("x")
    assert isinstance(m.id, Field)
    assert m.id._alias == "x"


def test_all_expression_operators():
    f = Field("x", int, "n")

    assert str(f + 1) == "(n.x + 1)"
    assert str(1 + f) == "(1 + n.x)"
    assert str(f * 2) == "(n.x * 2)"
    assert str(2 * f) == "(2 * n.x)"
    assert str(f / 3) == "(n.x / 3)"
    assert str(3 / f) == "(3 / n.x)"
    assert str(f - 4) == "(n.x - 4)"
    assert str(4 - f) == "(4 - n.x)"
    assert str(f < 5) == "(n.x < 5)"
    assert str(f <= 6) == "(n.x <= 6)"
    assert str(f > 7) == "(n.x > 7)"
    assert str(f >= 8) == "(8 <= n.x)"
    assert str(f == 9) == "(n.x = 9)"
    assert str(f != 10) == "(n.x <> 10)"
    assert str((f == 1) & (f != 2)) == "((n.x = 1) AND (n.x <> 2))"
    assert str((f > 1) | (f < 10)) == "((n.x > 1) OR (n.x < 10))"

class Line(TableModel):
    quantity: int


class Node(TableModel):
    total_input: int

def test_cross_model_expression():
    l = Line("l")
    n = Node("n")

    expr = l.quantity > n.total_input
    assert str(expr) == "(l.quantity > n.total_input)"

    # More complex case:
    complex_expr = (l.quantity > n.total_input) & (l.quantity < 100)
    assert str(complex_expr) == "((l.quantity > n.total_input) AND (l.quantity < 100))"
