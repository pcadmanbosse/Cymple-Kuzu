from cymple import QueryBuilder

from ..data.onto_types.labels import labels
from ..data.onto_types.properties import Properties
from ..data.onto_types.relations import Relations


def cypher_get_all_findings():
    output_mapping = [('n', 'n')]
    query = QueryBuilder().match().node(labels.Finding, 'n').return_mapping(output_mapping).get()
    return query


def cypher_get_findings():
    output_mapping = [(f'f.{Properties.has_id}', 'id'),
                      (f't.{Properties.has_probability}', 'probability'),
                      (f't.{Properties.has_severity}', 'severity'),
                      (f'ct.{Properties.has_id}', 'cve')]

    query = (QueryBuilder().match()
             .node(labels.Finding, 'f')
             .related_to(Relations.has_finding_type)
             .node(labels.FindingType, 't')
             .related_to(Relations.has_cve)
             .node(labels.CVEType, 'ct')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_services():
    output_mapping = [(f's.{Properties.has_id}', 'id'),
                      (f's.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(labels.ServiceType, 's')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_identities():
    output_mapping = [(f'i.{Properties.has_id}', 'id'),
                      (f'i.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(labels.Identity, 'i')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_business_applications():
    output_mapping = [(f'a.{Properties.has_id}', 'id'),
                      (f'a.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(labels.Application, 'a')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_finding_detailed(finding_id):
    output_mapping = [(f'f.{Properties.has_id}', 'id'),
                      (f't.{Properties.has_probability}', 'probability'),
                      (f't.{Properties.has_severity}', 'severity'),
                      (f'ct.{Properties.has_id}', 'cve'),
                      (f't.{Properties.has_description}', 'description'),
                      (f't.{Properties.has_attack_scenario}', 'attack_scenario'),
                      (f't.recommendation', 'recommendations')]

    query = (QueryBuilder().match()
             .node(labels.Finding, 'f', {Properties.has_id: finding_id})
             .related_to(Relations.has_finding_type)
             .node(labels.FindingType, 't')
             .related_to(Relations.has_cve)
             .node(labels.CVEType, 'ct')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_business_application(application_id):
    output_mapping = [(f'a.{Properties.has_id}', 'id'),
                      (f'a.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(labels.Application, 'a', {Properties.has_id: application_id})
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_references_for_finding(finding_id):
    output_mapping = [(f'r.{Properties.has_description}', 'reference')]

    query = (QueryBuilder().match()
             .node(labels.Finding, None, {Properties.has_id: finding_id})
             .related_to(Relations.has_reference)
             .node(labels.ReferenceType, 'r')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_applications_for_finding(finding_id):
    output_mapping = [(f'a.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(labels.Finding, None, {Properties.has_id: finding_id})
             .related_to(Relations.has_cloud_object)
             .node(labels.Application, 'a')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_finding_type_details_per_id(id):
    output_mapping = [(f'collect(t.{Properties.has_severity})', 'severities'),
                      (f'collect(t.{Properties.has_probability})', 'probabilities')]

    query = (QueryBuilder().match()
             .node(labels.FindingType, 't')
             .related_from(Relations.has_finding_type)
             .node(labels.Finding)
             .related_to(Relations.has_cloud_object)
             .node(labels.CloudObject)
             .related_to(Relations.has_service)
             .node(None, None, {Properties.has_id: id})
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_finding_details_for_application(application_id):
    output_mapping = [(f'f.{Properties.has_id}', 'id'),
                      (f't.{Properties.has_probability}', 'probability'),
                      (f't.{Properties.has_severity}', 'severity'),
                      (f'ct.{Properties.has_id}', 'cve')]

    query = (QueryBuilder().match()
             .node(labels.Application, None, {Properties.has_id: application_id})
             .related_to(Relations.has_cloud_object)
             .node(labels.CloudObject)
             .related_from(Relations.has_cloud_object)
             .node(labels.Finding, 'f')
             .related_to(Relations.has_finding_type)
             .node(labels.FindingType, 't')
             .related_to(Relations.has_cve)
             .node(labels.CVEType, 'ct')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_service_details_for_application(application_id):
    output_mapping = [(f's.{Properties.has_id}', 'id'),
                      (f's.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(labels.Application, None, {Properties.has_id: application_id})
             .related_to(Relations.has_cloud_object)
             .node(labels.CloudObject)
             .related_to(Relations.has_service)
             .node(labels.ServiceType, 's')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_match_set_id(service_id):
    query = (QueryBuilder().match()
             .node(labels.ServiceType, 's')
             .set({Properties.has_id: service_id})
             .return_literal('s')
             .get())

    return query


def cypher_merge_on_match(service_id):
    query = (QueryBuilder().merge()
             .node(labels.ServiceType, 's')
             .on_match()
             .set({Properties.has_id: service_id})
             .return_literal('s')
             .get())

    return query


def cypher_relationship_properties(service_id):
    query = (QueryBuilder().match()
             .node(labels.Application)
             .related_to(Relations.has_cloud_object)
             .node(labels.CloudObject)
             .related_to(Relations.has_service, properties={Properties.has_id: service_id})
             .node(labels.ServiceType, 's', {Properties.has_id: service_id})
             .return_literal('s')
             .get())

    return query


def test_cypher_get_all_findings():
    expected_query = f'MATCH (n: {labels.Finding}) RETURN n AS n'
    actual_query = cypher_get_all_findings()
    assert actual_query == expected_query


def test_cypher_get_findings():
    expected_query = (
        f'MATCH (f: {labels.Finding})-[: {Relations.has_finding_type}]->'
        f'(t: {labels.FindingType})-[: {Relations.has_cve}]->(ct: {labels.CVEType}) '
        f'RETURN f.{Properties.has_id} AS id, t.{Properties.has_probability} AS probability, '
        f't.{Properties.has_severity} AS severity, ct.{Properties.has_id} AS cve')
    actual_query = cypher_get_findings()
    assert actual_query == expected_query


def test_cypher_get_services():
    expected_query = (f'MATCH (s: {labels.ServiceType}) '
                      f'RETURN s.{Properties.has_id} AS id, s.{Properties.has_name} AS name')
    actual_query = cypher_get_services()
    assert actual_query == expected_query


def test_cypher_get_business_applications():
    expected_query = (f'MATCH (a: {labels.Application}) '
                      f'RETURN a.{Properties.has_id} AS id, a.{Properties.has_name} AS name')
    actual_query = cypher_get_business_applications()
    assert actual_query == expected_query


def test_cypher_get_finding_detailed():
    finding_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (f: {labels.Finding} {{{Properties.has_id} : "{finding_id}"}})-'
        f'[: {Relations.has_finding_type}]->(t: {labels.FindingType})'
        f'-[: {Relations.has_cve}]->(ct: {labels.CVEType}) '
        f'RETURN f.{Properties.has_id} AS id, '
        f't.{Properties.has_probability} AS probability, '
        f't.{Properties.has_severity} AS severity, ct.{Properties.has_id} AS cve, '
        f't.{Properties.has_description} AS description, '
        f't.{Properties.has_attack_scenario} AS attack_scenario, t.recommendation AS recommendations')

    actual_query = cypher_get_finding_detailed(finding_id)
    assert actual_query == expected_query


def test_cypher_get_business_application():
    application_id = 'THAT_is_MOCK_id'
    expected_query = (f'MATCH (a: {labels.Application} {{{Properties.has_id} : "{application_id}"}}) '
                      f'RETURN a.{Properties.has_id} AS id, a.{Properties.has_name} AS name')
    actual_query = cypher_get_business_application(application_id)
    assert actual_query == expected_query


def test_cypher_get_references_for_finding():
    finding_id = 'THAT_is_MOCK_id'

    expected_query = (f'MATCH (: {labels.Finding} {{{Properties.has_id} : "{finding_id}"}})'
                      f'-[: {Relations.has_reference}]->(r: {labels.ReferenceType}) '
                      f'RETURN r.{Properties.has_description} AS reference')

    actual_query = cypher_get_references_for_finding(finding_id)
    assert actual_query == expected_query


def test_cypher_get_applications_for_finding():
    finding_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (: {labels.Finding} {{{Properties.has_id} : "{finding_id}"}})'
        f'-[: {Relations.has_cloud_object}]->(a: {labels.Application}) '
        f'RETURN a.{Properties.has_name} AS name')

    actual_query = cypher_get_applications_for_finding(finding_id)
    assert actual_query == expected_query


def test_cypher_get_finding_type_details_for_service():
    service_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (t: {labels.FindingType})<-[: {Relations.has_finding_type}]-'
        f'(: {labels.Finding})-[: {Relations.has_cloud_object}]->'
        f'(: {labels.CloudObject})-[: {Relations.has_service}]->( {{{Properties.has_id} : "{service_id}"}}) '
        f'RETURN collect(t.{Properties.has_severity}) AS severities, '
        f'collect(t.{Properties.has_probability}) AS probabilities')

    actual_query = cypher_get_finding_type_details_per_id(service_id)
    assert actual_query == expected_query


def test_cypher_match_set_id():
    service_id = 'THAT_is_MOCK_id'

    expected_query = f'MATCH (s: {labels.ServiceType}) SET {Properties.has_id} = "{service_id}" RETURN s'

    actual_query = cypher_match_set_id(service_id)
    assert actual_query == expected_query


def test_cypher_merge_on_match():
    service_id = 'THAT_is_MOCK_id'

    expected_query = f'MERGE (s: {labels.ServiceType}) ON MATCH SET {Properties.has_id} = "{service_id}" RETURN s'

    actual_query = cypher_merge_on_match(service_id)
    assert actual_query == expected_query


def test_cypher_relationship_properties():
    service_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (: {labels.Application})-[: {Relations.has_cloud_object}]->'
        f'(: {labels.CloudObject})-[: {Relations.has_service} {{{Properties.has_id} : "{service_id}"}}]->'
        f'(s: {labels.ServiceType} {{{Properties.has_id} : "{service_id}"}}) RETURN s')

    actual_query = cypher_relationship_properties(service_id)
    assert actual_query == expected_query

def test_cypher_query_add():
    service_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (: {labels.Application})-[: {Relations.has_cloud_object}]->'
        f'(: {labels.CloudObject})-[: {Relations.has_service} {{{Properties.has_id} : "{service_id}"}}]->'
        f'(s: {labels.ServiceType} {{{Properties.has_id} : "{service_id}"}}) WITH s MATCH (s) RETURN s')

    actual_query1 = (QueryBuilder().match()
                    .node(labels.Application)
                    .related_to(Relations.has_cloud_object)
                    .node(labels.CloudObject)
                    .related_to(Relations.has_service, properties={Properties.has_id: service_id})
                    .node(labels.ServiceType, 's', {Properties.has_id: service_id})
                    .with_('s'))
    actual_query2 = (QueryBuilder().match()
                    .node(ref_name='s')
                    .return_literal('s'))

    actual_query = str(actual_query1 + actual_query2)
    assert actual_query == expected_query
    
    actual_query1 += actual_query2
    actual_query = str(actual_query1)
    assert actual_query == expected_query

def test_cypher_set_unescaped_after_merge():
    node_id = '1'

    expected_query = (
        f'MERGE (n: Node {{name : "test"}}) '
        f'ON CREATE SET n.id = "{node_id}" '
        f'ON MATCH SET n.id = n.id + "1" '
        f'RETURN n')

    actual_query = (QueryBuilder()
             .merge()
             .node('Node', 'n', {'name': 'test'})
             .on_create().set({f'n.id': node_id})
             .on_match().set({f'n.id': f'n.id + "1"'}, escape_values=False)
             .return_literal('n')
             .get())

    assert actual_query == expected_query

def test_multiple_where_1():
    expected_query = 'MATCH (p) WHERE p.lock IS NULL OR p.value IS NULL'
    actual_query = str(QueryBuilder().match().node(ref_name='p').where_multiple({'p.lock': 'NULL', 'p.value': 'NULL'}, 'IS', ' OR ', escape=False))
    assert actual_query == expected_query

def test_multiple_where_2():
    expected_query = 'MATCH (n: Person) WHERE n.age=32 AND NOT n:Teacher'
    actual_query = str(QueryBuilder().match().node('Person', ref_name='n').where_literal('n.age=32 AND NOT n:Teacher'))
    assert actual_query == expected_query

def test_with_list():
    expected_query = 'MATCH (n) WITH n AS n_test WITH [n_test] AS n_list RETURN n_list AS n_test'
    actual_query = str(QueryBuilder().match().node(ref_name='n').with_('n AS n_test').with_('[n_test] AS n_list').return_mapping(('n_list', 'n_test')))
    assert actual_query == expected_query