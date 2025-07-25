"""This is the Cymple query builder module."""

# pylint: disable=R0901
# pylint: disable=R0903
# pylint: disable=W0102
from typing import List, Union, Dict, Any
from .typedefs import Mapping, Properties

class Query():
    """A general query-descripting class ."""

    def __init__(self, query):
        """Initialize the query object."""
        self.query = query

    def __str__(self) -> str:
        """Implement the str() operator for the query builder."""
        return self.query.strip()

    def __add__(self, other):
        """Implement the + operator for the query builder."""
        return Query(self.query.strip() + ' ' + other.query.strip())

    def __iadd__(self, other):
        """Implement the += operator for the query builder."""
        self.query = self.query.strip() + ' ' + other.query.strip()
        return self

    def get(self):
        """Get the final query string ."""
        return str(self)

    def cypher(self, cypher_query_str):
        """Concatenate a cypher query string"""
        return AnyAvailable(self.query.strip() + ' ' + cypher_query_str.strip())


class QueryStart(Query):
    """A class for representing a "QUERY START" clause."""

class AddColumn(Query):
    """A class for representing a "ADD COLUMN" clause."""

    def add_column(self, name: str, type: str, primary_key: bool = False, if_not_exists: bool = True, default_value: any = None):
        """Add a column.
        
        :param name: The name of the column to add
        :type name: str
        :param type: The type of the column to add
        :type type: str
        :param primary_key: Is the column a primary key, defaults to False
        :type primary_key: bool
        :param if_not_exists: Add the IF NOT EXISTS flag, defaults to True
        :type if_not_exists: bool
        :param default_value: The default value of the column, defaults to None
        :type default_value: any
        
        :return: A Query object with a query that contains the new clause.
        :rtype: AddColumnAvailable
        """
        if_not_exists_part = " IF NOT EXISTS" if if_not_exists else ""
        default_part = f" DEFAULT {default_value}" if default_value is not None else ""
        primary_key_part = " PRIMARY KEY" if primary_key else ""
        query_part = f""" ADD{if_not_exists_part} {name} {type}{default_part}{primary_key_part}"""
        return AddColumnAvailable(self.query + query_part)

class Alter(Query):
    """A class for representing a "ALTER" clause."""

    def alter(self):
        """Concatenate the "ALTER" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: AlterAvailable
        """
        return AlterAvailable(self.query + ' ALTER')

class And(Query):
    """A class for representing a "AND" clause."""

    def and_(self, **kwargs):
        """Concatenate another clause, using a comma. E.G match (n), ...
        
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: AndAvailable
        """
        return AndAvailable(self.query + ",")

class Call(Query):
    """A class for representing a "CALL" clause."""

    def call(self):
        """Concatenate the "CALL" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: CallAvailable
        """
        return CallAvailable(self.query + ' CALL')

class Case(Query):
    """A class for representing a "CASE" clause."""

    def case(self, when_then_mapping: Dict[str, Union[List[str], str]], default_result: str, results_ref: str = None, test_expression: str = None):
        """Concatenate a CASE clause to the query, to compare a single expression against multiple values or to express multiple conditional statements.
        
        :param when_then_mapping: A dictionary such that a value represents a literal expression (or a list of
            expressions) whose result will be compared to test_expression if given, else is evaluated to a BOOLEAN, and it's key represents the literal expression returned as output if the value matches test_expression if giver, or if the expression evaluates to TRUE.
        :type when_then_mapping: Dict[str, Union[List[str], str]]
        :param default_result: The expression to return if no value matches the test expression if given, or if all
            expressions evaluated as FALSE.
        :type default_result: str
        :param results_ref: The reference name of the resulted returned values, plus any other desired reference names
            to return., defaults to None
        :type results_ref: str
        :param test_expression: An expression to test the cases against. For example, 'n.name'. Optional., defaults to
            None
        :type test_expression: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: CaseAvailable
        """
        ret = " CASE"
        if test_expression is not None:
            ret += f" {test_expression}"
        for then, when in when_then_mapping.items():
            if type(when) is not list:
                when = [when]
            ret += f" WHEN {', '.join(when)} THEN {then}"
        ret += f" ELSE {default_result} END"
        if results_ref is not None:
            ret += f" AS {results_ref}"
        return CaseAvailable(self.query + ret)

class CaseWhen(Query):
    """A class for representing a "CASE WHEN" clause."""

    def case_when(self, filters: dict, on_true: str, on_false: str, ref_name: str, comparison_operator: str = "=", boolean_operator: str = "AND", **kwargs):
        """Concatenate a CASE WHEN clause to the query, created from a list of given property filters.
        
        :param filters: A dict representing the set of properties to be filtered
        :type filters: dict
        :param on_true: The query to run when the predicate is true
        :type on_true: str
        :param on_false: The query to run when the predicate is false
        :type on_false: str
        :param ref_name: The name which is used to refer to the newly filtered object
        :type ref_name: str
        :param comparison_operator: A string operator, according to which the comparison between property values is
            done, e.g. for "=", we get: property.name = property.value, defaults to "="
        :type comparison_operator: str
        :param boolean_operator: The boolean operator to apply between predicates, defaults to "AND"
        :type boolean_operator: str
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: CaseWhenAvailable
        """
        filt = ' CASE WHEN ' + Properties(filters).to_str(comparison_operator, boolean_operator, **kwargs)
        filt += f' THEN {on_true} ELSE {on_false} END AS {ref_name}'
        return CaseWhenAvailable(self.query + filt)

class Create(Query):
    """A class for representing a "CREATE" clause."""

    def create(self):
        """Concatenate the "CREATE" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: CreateAvailable
        """
        return CreateAvailable(self.query + ' CREATE')

class Delete(Query):
    """A class for representing a "DELETE" clause."""

    def delete(self, ref_name: str):
        """Concatenate a DELETE clause for a referenced instance from the DB.
        
        :param ref_name: The reference name to be used for the delete operation
        :type ref_name: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: DeleteAvailable
        """
        ret = f' DELETE {ref_name}'
        return DeleteAvailable(self.query + ret)

    def detach_delete(self, ref_name: str):
        """Concatenate a DETACH DELETE clause for a referenced instance from the DB.
        
        :param ref_name: The reference name to be used for the delete operation
        :type ref_name: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: DeleteAvailable
        """
        ret = f' DETACH DELETE {ref_name}'
        return DeleteAvailable(self.query + ret)

class DropColumn(Query):
    """A class for representing a "DROP COLUMN" clause."""

    def drop_column(self, name: str, if_exists: bool = True):
        """A column to drop.
        
        :param name: The name of the column to drop
        :type name: str
        :param if_exists: Add the IF EXISTS flag, defaults to True
        :type if_exists: bool
        
        :return: A Query object with a query that contains the new clause.
        :rtype: DropColumnAvailable
        """
        return DropColumnAvailable(self.query + f""" DROP {"IF EXISTS " if if_exists else ""}{name}""")

class Limit(Query):
    """A class for representing a "LIMIT" clause."""

    def limit(self, limitation: Union[int, str]):
        """Concatenate a limit statement.
        
        :param limitation: A non-negative integer or a string of cypher expression that evaluates to a non-negative
            integer (as long as it is not referring to any external variables)
        :type limitation: Union[int, str]
        
        :return: A Query object with a query that contains the new clause.
        :rtype: LimitAvailable
        """
        ret = f" LIMIT {limitation}"
        return LimitAvailable(self.query + ret)

class Match(Query):
    """A class for representing a "MATCH" clause."""

    def match(self):
        """Concatenate the "MATCH" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: MatchAvailable
        """
        return MatchAvailable(self.query + ' MATCH')

    def match_optional(self):
        """Concatenate the "MATCH" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: MatchAvailable
        """
        return MatchAvailable(self.query + ' OPTIONAL MATCH ')

class Merge(Query):
    """A class for representing a "MERGE" clause."""

    def merge(self):
        """Concatenate the "MERGE" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: MergeAvailable
        """
        return MergeAvailable(self.query + ' MERGE')

class NewQuery(Query):
    """A class for representing a "NEW QUERY" clause."""

    def new_query(self):
        """Concatenate the "NEW QUERY" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: NewQueryAvailable
        """
        return NewQueryAvailable(self.query + f';')

class Node(Query):
    """A class for representing a "NODE" clause."""

    def node(self, labels: Union[List[str], str] = None, ref_name: str = None, properties: dict = None, **kwargs):
        """Concatenate a graph Node, which may be filtered using any labels/s and/or property/properties.
        
        :param labels: The labels(or list of labels) for that node, defaults to None
        :type labels: Union[List[str], str]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the nodes are filtered, defaults to None
        :type properties: dict
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: NodeAvailable
        """
        if not labels:
            labels_string = ''
        elif isinstance(labels, str):
            labels_string = f': {labels}'
        elif isinstance(labels, list):
            labels = [str(x) for x in labels]
            labels_string = f': {": ".join(labels).strip()}'
        else:
            labels_string = f':{str(labels)}'
    
    
        if not properties:
            property_string = ''
        else:
            property_string = f' {{{Properties(properties).to_str(**kwargs)}}}'
    
        ref_name = ref_name or ''
    
        query = self.query
        if not (query.endswith('-') or query.endswith('>') or query.endswith('<')):
            query += ' '
    
        query += f'({ref_name}{labels_string}{property_string})'
        
        if isinstance(self, MergeAvailable):
            return NodeAfterMergeAvailable(query)
    
        return NodeAvailable(query)

class NodeAfterMerge(Query):
    """A class for representing a "NODE AFTER MERGE" clause."""

    def node(self, labels: Union[List[str], str] = None, ref_name: str = None, properties: dict = None, **kwargs):
        """Concatenate a graph Node, which may be filtered using any labels/s and/or property/properties.
        
        :param labels: The labels(or list of labels) for that node, defaults to None
        :type labels: Union[List[str], str]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the nodes are filtered, defaults to None
        :type properties: dict
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: NodeAfterMergeAvailable
        """
        if not labels:
            labels_string = ''
        elif isinstance(labels, str):
            labels_string = f': {labels}'
        elif isinstance(labels, list):
            labels = [str(x) for x in labels]
            labels_string = f': {": ".join(labels).strip()}'
        else:
            labels_string = f':{str(labels)}'
    
    
        if not properties:
            property_string = ''
        else:
            property_string = f' {{{Properties(properties).to_str(**kwargs)}}}'
    
        ref_name = ref_name or ''
    
        query = self.query
        if not (query.endswith('-') or query.endswith('>') or query.endswith('<')):
            query += ' '
    
        query += f'({ref_name}{labels_string}{property_string})'
        
        if isinstance(self, MergeAvailable):
            return NodeAfterMergeAvailable(query)
    
        return NodeAvailable(query)

class OnCreate(Query):
    """A class for representing a "ON CREATE" clause."""

    def on_create(self):
        """Concatenate the "ON CREATE" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: OnCreateAvailable
        """
        return OnCreateAvailable(self.query + ' ON CREATE')

class OnMatch(Query):
    """A class for representing a "ON MATCH" clause."""

    def on_match(self):
        """Concatenate the "ON MATCH" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: OnMatchAvailable
        """
        return OnMatchAvailable(self.query + ' ON MATCH')

class OperatorEnd(Query):
    """A class for representing a "OPERATOR END" clause."""

    def operator_end(self):
        """Concatenate the "OPERATOR END" clause.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: OperatorEndAvailable
        """
        return OperatorEndAvailable(self.query + ' )')

class OperatorStart(Query):
    """A class for representing a "OPERATOR START" clause."""

    def operator_start(self, operator: str, ref_name: str = None, args: dict = None):
        """Concatenate an operator (e.g. ShortestPath), where its result may be given a name for future reference.
        
        :param operator: The operator to be used (e.g. ShortestPath)
        :type operator: str
        :param ref_name: A reference name of the result, to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param args: A dict of arguments, to be passed to the operator function, defaults to None
        :type args: dict
        
        :return: A Query object with a query that contains the new clause.
        :rtype: OperatorStartAvailable
        """
        result_name = '' if ref_name is None else f'{ref_name} = '
        arguments = '' if args is None else f' {args}'
    
        return OperatorStartAvailable(self.query + f' {result_name}{operator}({arguments}')

class OrderBy(Query):
    """A class for representing a "ORDER BY" clause."""

    def order_by(self, sorting_properties: Union[str, List[str]], ascending: bool = True):
        """Concatenate an order by statement.
        
        :param sorting_properties: A string or a list of strings representing the properties based on which to sort.
        :type sorting_properties: Union[str, List[str]]
        :param ascending: Use ascending sorting (if false, uses descending)., defaults to True
        :type ascending: bool
        
        :return: A Query object with a query that contains the new clause.
        :rtype: OrderByAvailable
        """
        if type(sorting_properties) != list:
            sorting_properties = [sorting_properties]
    
        ret = f" ORDER BY {', '.join(sorting_properties)}"
        ret += " ASC" if ascending else " DESC"
        return OrderByAvailable(self.query + ret)

class Path(Query):
    """A class for representing a "PATH" clause."""

    def path(self, ref_name: str):
        """Concatenate a {ref_name} = path clause, to use later in the query.
        
        :param ref_name: A reference name to be used later in the rest of the query
        :type ref_name: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: PathAvailable
        """
        return MatchAvailable(self.query + f' {ref_name} =')

class Procedure(Query):
    """A class for representing a "PROCEDURE" clause."""

    def procedure(self, literal_procedure: str):
        """Concatenate a literal procedure.
        
        :param literal_procedure: A string that is evaluated to a cypher procedure
        :type literal_procedure: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: ProcedureAvailable
        """
        ret = f" {literal_procedure}"
        return ProcedureAvailable(self.query + ret)

class Relation(Query):
    """A class for representing a "RELATION" clause."""

    def related(self, labels: Union[str, List[str]] = None, ref_name: str = None, properties: dict = None, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate an undirectional (i.e. --) graph Relationship, which may be filtered.
        
        :param labels: The relationship labels(type or types) in the DB, defaults to None
        :type labels: Union[str, List[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            None
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('none', labels, ref_name, properties, min_hops, max_hops, shortest, **kwargs))

    def related_to(self, labels: Union[str, List[str]] = None, ref_name: str = None, properties: dict = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate a forward (i.e. -->) graph Relationship, which may be filtered.
        
        :param labels: The relationship labels(type or types) in the DB, defaults to None
        :type labels: Union[str, List[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            {}
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('forward', labels, ref_name, properties, min_hops, max_hops, shortest, **kwargs))

    def related_from(self, labels: Union[str, List[str]] = None, ref_name: str = None, properties: dict = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate a backward (i.e. <--) graph Relationship, which may be filtered.
        
        :param labels: The relationship labels(type or types) in the DB, defaults to None
        :type labels: Union[str, List[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            {}
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('backward', labels, ref_name, properties, min_hops, max_hops, shortest, **kwargs))

    def _directed_relation(self, direction: str, labels: Union[str, List[str]], ref_name: str = None, properties: dict = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate a graph Relationship (private method).
        
        :param direction: The relationship direction, can one of 'forward', 'backward' - otherwise unidirectional
        :type direction: str
        :param labels: The relationship labels(type or types) in the DB
        :type labels: Union[str, List[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            {}
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        min_hops_str = '' if min_hops == -1 else str(min_hops)
        max_hops_str = '' if max_hops == -1 else str(max_hops)
    
        if isinstance(labels, list):
            relation_type = "|".join([f':{l}' for l in labels])
        else:
            relation_type = '' if labels is None else f': {labels}'
        relation_ref_name = '' if ref_name is None else f'{ref_name}'
        relation_properties = f' {{{Properties(properties).to_str(**kwargs)}}}' if properties else ''
    
        if min_hops == 1 and max_hops == 1:
            relation_length = ''
        else:
            relation_length = '*'
            if shortest and not (min_hops == 1 and max_hops == 1):
                if shortest == 'all':
                    relation_length += "ALL SHORTEST "
                else:
                    relation_length += "SHORTEST "
    
            if min_hops == max_hops:
                if min_hops != -1:
                    relation_length += f'{min_hops_str}'
            else:
                relation_length += f'{min_hops_str}..{max_hops_str}'
    
        if relation_ref_name or relation_type or relation_length or relation_properties:
            relation_str = f'[{relation_ref_name}{relation_type}{relation_length}{relation_properties}]'
        else:
            relation_str = ''
    
        if direction == 'forward':
            return f'-{relation_str}->'
        if direction == 'backward':
            return f'<-{relation_str}-'
    
        return f'-{relation_str}-'

class RelationAfterMerge(Query):
    """A class for representing a "RELATION AFTER MERGE" clause."""

    def related(self, labels: Union[str, list[str]] = None, ref_name: str = None, properties: dict = None, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate an undirectional (i.e. --) graph Relationship, which may be filtered.
        
        :param labels: The relationship labels(type or types) in the DB, defaults to None
        :type labels: Union[str, list[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            None
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAfterMergeAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('none', labels, ref_name, properties, min_hops, max_hops, shortest, **kwargs))

    def related_to(self, labels: Union[str, list[str]] = None, ref_name: str = None, properties: dict = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate a forward (i.e. -->) graph Relationship, which may be filtered.
        
        :param labels: The relationship labels(type or types) in the DB, defaults to None
        :type labels: Union[str, list[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            {}
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAfterMergeAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('forward', labels, ref_name, properties, min_hops, max_hops, shortest, **kwargs))

    def related_from(self, labels: Union[str, list[str]] = None, ref_name: str = None, properties: dict = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate a backward (i.e. <--) graph Relationship, which may be filtered.
        
        :param labels: The relationship labels(type or types) in the DB, defaults to None
        :type labels: Union[str, list[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            {}
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAfterMergeAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('backward', labels, ref_name, properties, min_hops, max_hops, shortest, **kwargs))

    def _directed_relation(self, direction: str, labels: Union[str, list[str]], ref_name: str = None, properties: dict = {}, min_hops: int = 1, max_hops: int = 1, shortest: Union[bool, str] = False, **kwargs):
        """Concatenate a graph Relationship (private method).
        
        :param direction: The relationship direction, can one of 'forward', 'backward' - otherwise unidirectional
        :type direction: str
        :param labels: The relationship labels(type or types) in the DB
        :type labels: Union[str, list[str]]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A dict representing the set of properties by which the relationship is filtered, defaults to
            {}
        :type properties: dict
        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to 1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to 1
        :type max_hops: int
        :param shortest: Whether to add the SHORTEST flag to a recursive relationship. Requires min_hops | max_hops.
            Can be True/'shortest' for SHORTEST, or 'all' for ALL SHORTEST, defaults to False
        :type shortest: Union[bool, str]
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAfterMergeAvailable
        """
        min_hops_str = '' if min_hops == -1 else str(min_hops)
        max_hops_str = '' if max_hops == -1 else str(max_hops)
    
        if isinstance(labels, list):
            relation_type = "|".join([f':{l}' for l in labels])
        else:
            relation_type = '' if labels is None else f': {labels}'
        relation_ref_name = '' if ref_name is None else f'{ref_name}'
        relation_properties = f' {{{Properties(properties).to_str(**kwargs)}}}' if properties else ''
    
        if min_hops == 1 and max_hops == 1:
            relation_length = ''
        else:
            relation_length = '*'
            if shortest and not (min_hops == 1 and max_hops == 1):
                if shortest == 'all':
                    relation_length += "ALL SHORTEST "
                else:
                    relation_length += "SHORTEST "
    
            if min_hops == max_hops:
                if min_hops != -1:
                    relation_length += f'{min_hops_str}'
            else:
                relation_length += f'{min_hops_str}..{max_hops_str}'
    
        if relation_ref_name or relation_type or relation_length or relation_properties:
            relation_str = f'[{relation_ref_name}{relation_type}{relation_length}{relation_properties}]'
        else:
            relation_str = ''
    
        if direction == 'forward':
            return f'-{relation_str}->'
        if direction == 'backward':
            return f'<-{relation_str}-'
    
        return f'-{relation_str}-'

class Remove(Query):
    """A class for representing a "REMOVE" clause."""

    def remove(self, properties: Union[str, List[str]]):
        """Concatenate a remove by statement.
        
        :param properties: A string or a list of strings representing the properties to remove.
        :type properties: Union[str, List[str]]
        
        :return: A Query object with a query that contains the new clause.
        :rtype: RemoveAvailable
        """
        if type(properties) != list:
            properties = [properties]
        ret = f" REMOVE {', '.join(properties)}"
        return RemoveAvailable(self.query + ret)

class Return(Query):
    """A class for representing a "RETURN" clause."""

    def return_literal(self, literal: str = None):
        """Concatenate a literal RETURN statement.
        
        :param literal: A Cypher string describing the objects to be returned, referencing name/names which were
            defined earlier in the query, defaults to None
        :type literal: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: ReturnAvailable
        """
        ret = f' RETURN'
        if literal is not None:
            literal = str(literal)
            ret += f' {literal}'
    
        return ReturnAvailable(self.query + ret)

    def return_mapping(self, mappings: List[Mapping]):
        """Concatenate a RETURN statement for multiple objects.
        
        :param mappings: The mapping (or a list of mappings) of db property names to code names, to be returned
        :type mappings: List[Mapping]
        
        :return: A Query object with a query that contains the new clause.
        :rtype: ReturnAvailable
        """
        if not isinstance(mappings, list):
            mappings = [mappings]
    
        ret = ' RETURN ' + \
            ', '.join(
                f'{mapping[0]} AS {mapping[1]}' if mapping[1] else mapping[0].replace(".", "_")
                for mapping in mappings)
    
        return ReturnAvailable(self.query + ret)

class Set(Query):
    """A class for representing a "SET" clause."""

    def set(self, properties: dict, escape_values: bool = True):
        """Concatenate a SET clause, using the given properties map.
        
        :param properties: A dict to be used to set the variables with their corresponding values
        :type properties: dict
        :param escape_values: Determines whether the properties values should be escaped or not, defaults to True
        :type escape_values: bool
        
        :return: A Query object with a query that contains the new clause.
        :rtype: SetAvailable
        """
        if isinstance(properties, dict):
            _properties = Properties(properties).to_str("=", ", ", escape_values)
        else:
            _properties = str(properties)
        
        query = self.query + ' SET ' + _properties
        
        if isinstance(self, NodeAfterMergeAvailable) or isinstance(self, OnCreateAvailable) or isinstance(self, OnMatchAvailable) or isinstance(self, SetAfterMergeAvailable):
            return SetAfterMergeAvailable(query)
    
        return SetAvailable(query)

class SetAfterMerge(Query):
    """A class for representing a "SET AFTER MERGE" clause."""

    def set(self, properties: dict, escape_values: bool = True):
        """Concatenate a SET clause, using the given properties map.
        
        :param properties: A dict to be used to set the variables with their corresponding values
        :type properties: dict
        :param escape_values: Determines whether the properties values should be escaped or not, defaults to True
        :type escape_values: bool
        
        :return: A Query object with a query that contains the new clause.
        :rtype: SetAfterMergeAvailable
        """
        if isinstance(properties, dict):
            _properties = Properties(properties).to_str("=", ", ", escape_values)
        else:
            _properties = str(properties)
        
        query = self.query + ' SET ' + _properties
        
        if isinstance(self, NodeAfterMergeAvailable) or isinstance(self, OnCreateAvailable) or isinstance(self, OnMatchAvailable) or isinstance(self, SetAfterMergeAvailable):
            return SetAfterMergeAvailable(query)
    
        return SetAvailable(query)

class Skip(Query):
    """A class for representing a "SKIP" clause."""

    def skip(self, skip_count: Union[int, str]):
        """Concatenate a skip statement.
        
        :param skip_count: A non-negative integer or a string of cypher expression that evaluates to a non-negative
            integer (as long as it is not referring to any external variables)
        :type skip_count: Union[int, str]
        
        :return: A Query object with a query that contains the new clause.
        :rtype: SkipAvailable
        """
        ret = f" SKIP {skip_count}"
        return SkipAvailable(self.query + ret)

class Table(Query):
    """A class for representing a "TABLE" clause."""

    def table(self, name: str):
        """Add a table statement.
        
        :param name: The name of the table
        :type name: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: TableAvailable
        """
        return TableAvailable(self.query + f' TABLE {name}')

class Union(Query):
    """A class for representing a "UNION" clause."""

    def union(self):
        """Combines the results of two or more queries. Duplicates are removed.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: UnionAvailable
        """
        return UnionAvailable(self.query + f' UNION')

    def union_all(self):
        """Combines the results of two or more queries including duplicates.
        
        :return: A Query object with a query that contains the new clause.
        :rtype: UnionAvailable
        """
        return UnionAvailable(self.query + f' UNION ALL')

class Unwind(Query):
    """A class for representing a "UNWIND" clause."""

    def unwind(self, variables: str):
        """Concatenate an UNWIND clause, keeping one or more variables given in 'variables' arg.
        
        :param variables: A string refering to previously obtained variables, comma seperated
        :type variables: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: UnwindAvailable
        """
        return UnwindAvailable(self.query + f' UNWIND {variables}')

class Where(Query):
    """A class for representing a "WHERE" clause."""

    def where(self, name: str, comparison_operator: str, value: str, **kwargs):
        """Concatenate a WHERE clause to the query, created as {name} {comparison_operator} {value}. E.g. x = 'abc'.
        
        :param name: The name of the object which is to be used in the comparison
        :type name: str
        :param comparison_operator: A string operator, according to which the comparison between compared object and
            the {value} is done, e.g. for "=", we get: {name} = {value}
        :type comparison_operator: str
        :param value: The value which is compared against
        :type value: str
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: WhereAvailable
        """
        return self.where_multiple({name: value}, comparison_operator, **kwargs)

    def where_multiple(self, filters: dict, comparison_operator: str = "=", boolean_operator: str = ' AND ', **kwargs):
        """Concatenate a WHERE clause to the query, created from a list of given property filters.
        
        :param filters: A dict representing the set of properties to be filtered
        :type filters: dict
        :param comparison_operator: A string operator, according to which the comparison between property values is
            done, e.g. for "=", we get: property.name = property.value, defaults to "="
        :type comparison_operator: str
        :param boolean_operator: The boolean operator to apply between predicates, defaults to ' AND '
        :type boolean_operator: str
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: WhereAvailable
        """
        filt = ' WHERE ' + Properties(filters).to_str(comparison_operator, boolean_operator, **kwargs)
        return WhereAvailable(self.query + filt)

    def where_literal(self, statement: str, **kwargs):
        """Concatenate a literal WHERE clause to the query.
        
        :param statement: A literal string of the required filter
        :type statement: str
        :param **kwargs: kwargs
        :type **kwargs
        
        :return: A Query object with a query that contains the new clause.
        :rtype: WhereAvailable
        """
        statement = str(statement)
        filt = ' WHERE ' + statement
        return WhereAvailable(self.query + filt)

class With(Query):
    """A class for representing a "WITH" clause."""

    def with_(self, variables: str):
        """Concatenate a WITH clause, keeping one or more variables given in 'variables' arg.
        
        :param variables: A string refering to previously obtained variables, comma seperated
        :type variables: str
        
        :return: A Query object with a query that contains the new clause.
        :rtype: WithAvailable
        """
        return WithAvailable(self.query + f' WITH {variables}')

class Yield(Query):
    """A class for representing a "YIELD" clause."""

    def yield_(self, mappings: List[Mapping]):
        """Concatenate a YIELD cluase, to yield a list of Mappings.
        
        :param mappings: The list of mappings of db properties names to code names, to be yielded
        :type mappings: List[Mapping]
        
        :return: A Query object with a query that contains the new clause.
        :rtype: YieldAvailable
        """
        if not isinstance(mappings, list):
            mappings = [mappings]
        
        query = ' YIELD ' + \
            ', '.join(f'{mapping[0]} AS '
                      f'{mapping[1] if mapping[1] else mapping[0].replace(".", "_")}'
                      for mapping in mappings)
        return YieldAvailable(self.query + query)


class QueryStartAvailable(Match, Merge, Call, Create, With, Alter):
    """A class decorator declares a QueryStart is available in the current query."""

class AddColumnAvailable(NewQuery):
    """A class decorator declares a AddColumn is available in the current query."""

class AlterAvailable(Table):
    """A class decorator declares a Alter is available in the current query."""

class AndAvailable(Node, Path):
    """A class decorator declares a And is available in the current query."""

class CallAvailable(Procedure):
    """A class decorator declares a Call is available in the current query."""

class CaseAvailable(QueryStartAvailable, Unwind, Where, Set, Remove, CaseWhen, Return, Limit, Skip, OrderBy, Union):
    """A class decorator declares a Case is available in the current query."""

class CaseWhenAvailable(QueryStartAvailable, Unwind, Where, CaseWhen, Return, Set):
    """A class decorator declares a CaseWhen is available in the current query."""

class CreateAvailable(Node, Union):
    """A class decorator declares a Create is available in the current query."""

class DeleteAvailable(Return, CaseWhen, Union):
    """A class decorator declares a Delete is available in the current query."""

class DropColumnAvailable(NewQuery):
    """A class decorator declares a DropColumn is available in the current query."""

class LimitAvailable(QueryStartAvailable, Unwind, Where, CaseWhen, Return, Set, Skip, Union):
    """A class decorator declares a Limit is available in the current query."""

class MatchAvailable(Node, Return, OperatorStart, Path):
    """A class decorator declares a Match is available in the current query."""

class MergeAvailable(NodeAfterMerge, Return, OperatorStart, Union):
    """A class decorator declares a Merge is available in the current query."""

class NewQueryAvailable(QueryStartAvailable):
    """A class decorator declares a NewQuery is available in the current query."""

class NodeAvailable(Relation, Return, Delete, Where, OperatorStart, OperatorEnd, Set, QueryStartAvailable, Merge, Remove, And):
    """A class decorator declares a Node is available in the current query."""

class NodeAfterMergeAvailable(RelationAfterMerge, Return, Delete, OperatorStart, OperatorEnd, SetAfterMerge, OnCreate, OnMatch, QueryStartAvailable):
    """A class decorator declares a NodeAfterMerge is available in the current query."""

class OnCreateAvailable(SetAfterMerge, OperatorStart):
    """A class decorator declares a OnCreate is available in the current query."""

class OnMatchAvailable(SetAfterMerge, OperatorStart):
    """A class decorator declares a OnMatch is available in the current query."""

class OperatorEndAvailable(QueryStartAvailable, Yield, With, Return):
    """A class decorator declares a OperatorEnd is available in the current query."""

class OperatorStartAvailable(QueryStartAvailable, Node, OperatorEnd):
    """A class decorator declares a OperatorStart is available in the current query."""

class OrderByAvailable(Limit, Skip, Union):
    """A class decorator declares a OrderBy is available in the current query."""

class PathAvailable(Node, OperatorStart):
    """A class decorator declares a Path is available in the current query."""

class ProcedureAvailable(Yield, Return, QueryStartAvailable, Union):
    """A class decorator declares a Procedure is available in the current query."""

class RelationAvailable(Node):
    """A class decorator declares a Relation is available in the current query."""

class RelationAfterMergeAvailable(NodeAfterMerge):
    """A class decorator declares a RelationAfterMerge is available in the current query."""

class RemoveAvailable(Set, Return, Union):
    """A class decorator declares a Remove is available in the current query."""

class ReturnAvailable(QueryStartAvailable, Unwind, Return, Limit, Skip, OrderBy, Union, CaseWhen, Case):
    """A class decorator declares a Return is available in the current query."""

class SetAvailable(QueryStartAvailable, Set, Remove, Unwind, Return, Union):
    """A class decorator declares a Set is available in the current query."""

class SetAfterMergeAvailable(QueryStartAvailable, OnCreate, OnMatch, SetAfterMerge, Unwind, Return, Union):
    """A class decorator declares a SetAfterMerge is available in the current query."""

class SkipAvailable(QueryStartAvailable, Unwind, Where, CaseWhen, Return, Set, Remove, Limit, Union):
    """A class decorator declares a Skip is available in the current query."""

class TableAvailable(AddColumn, DropColumn):
    """A class decorator declares a Table is available in the current query."""

class UnionAvailable(Call, Create, Delete, Match, Merge, Remove, Return, Set, Unwind, With):
    """A class decorator declares a Union is available in the current query."""

class UnwindAvailable(QueryStartAvailable, Unwind, Return, Create, Remove):
    """A class decorator declares a Unwind is available in the current query."""

class WhereAvailable(Return, Delete, Where, Set, Remove, OperatorStart, QueryStartAvailable):
    """A class decorator declares a Where is available in the current query."""

class WithAvailable(QueryStartAvailable, Unwind, Where, Set, Remove, CaseWhen, Return, Limit, Skip, OrderBy, Case):
    """A class decorator declares a With is available in the current query."""

class YieldAvailable(QueryStartAvailable, Node, Where, Return):
    """A class decorator declares a Yield is available in the current query."""

class AnyAvailable(AddColumn, Alter, And, Call, Case, CaseWhen, Create, Delete, DropColumn, Limit, Match, Merge, NewQuery, Node, NodeAfterMerge, OnCreate, OnMatch, OperatorEnd, OperatorStart, OrderBy, Path, Procedure, QueryStart, Relation, RelationAfterMerge, Remove, Return, Set, SetAfterMerge, Skip, Table, Union, Unwind, Where, With, Yield):
    """A class decorator declares anything is available in the current query."""

class QueryBuilder(QueryStartAvailable):
    """The Query Builder's initial interface."""

    def __init__(self) -> None:
        """Initialize a query builder."""
        super().__init__('')

    def reset(self):
        """Reset the query to an empty string."""
        self.query = ''
        return self
