from datetime import datetime
import pytest
from cymple import QueryBuilder
from cymple.table_model import TableModel

qb = QueryBuilder()

class Node(TableModel):
    attribute_1 : int
    attribute_2: str
    attribute_3: datetime
    attribute_4: float

class Rel(TableModel):
    attribute_1 : int
    attribute_2: str
    attribute_3: datetime
    attribute_4: float

n = Node("n")
r = Rel("r")

rendered = {
    '_RESET_': qb.reset(),
    'ALTER TABLE (add)': qb.reset().alter().table(Node).add_column(name="bool_col", type="BOOL", primary_key=True, default_value="True"),
    'CASE WHEN': qb.reset().match().node(ref_name=n).with_(n).case_when({f'{n.attribute_1}': 'Bob'}, 'true', 'false', 'my_boolean'),
    'DELETE': qb.reset().match().node(ref_name=n).delete(n),
    'DETACH DELETE': qb.reset().match().node(ref_name=n).detach_delete('n'),
    'WHERE (single)': qb.reset().match().node(ref_name=n).where(f'{n.attribute_1}', '=', 'value'),
    'WHERE (multiple)': qb.reset().match().node(ref_name=n).where_multiple({f'{n.attribute_1}': 'value', f'{n.attribute_2}': 20}),
    'WHERE (literal)': qb.reset().match().node(ref_name=n, properties={Node.attribute_1: 10, Node.attribute_2: 10}).where_literal((n.attribute_2 == "10") & (n.attribute_2 >= 3) & (n.attribute_3 != r.attribute_3)),
    'WHERE (mix of instance and class references)': qb.reset().match().node(Node, n).where_literal((n.attribute_2 == "10") & (n.attribute_2 >= 3)).return_literal(f"sum({n.attribute_1 + n.attribute_2})")
}

expected = {
    '_RESET_': '',
    'ALTER TABLE (add)': "ALTER TABLE NODE ADD IF NOT EXISTS bool_col BOOL DEFAULT True PRIMARY KEY",
    'CASE WHEN': 'MATCH (n) WITH n CASE WHEN n.attribute_1 = "Bob" THEN true ELSE false END AS my_boolean',
    'DELETE': 'MATCH (n) DELETE n',
    'DETACH DELETE': 'MATCH (n) DETACH DELETE n',
    'WHERE (single)': 'MATCH (n) WHERE n.attribute_1 = "value"',
    'WHERE (multiple)': 'MATCH (n) WHERE n.attribute_1 = "value" AND n.attribute_2 = 20',
    'WHERE (literal)': 'MATCH (n {attribute_1 : 10, attribute_2 : 10}) WHERE (((n.attribute_2 = \'10\') AND (3 <= n.attribute_2)) AND (n.attribute_3 <> r.attribute_3))',
    'WHERE (mix of instance and class references)': "MATCH (n:NODE) WHERE ((n.attribute_2 = '10') AND (3 <= n.attribute_2)) RETURN sum((n.attribute_1 + n.attribute_2))"
}


@pytest.mark.parametrize('clause', expected)
def test_case(clause: str):
    assert str(rendered[clause]) == expected[clause]
