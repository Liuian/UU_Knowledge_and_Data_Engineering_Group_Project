from rdflib import Graph, RDF, RDFS, OWL
import os
import pandas as pd

rdf = "./data/wiki_db_cleaned.ttl"
ontology = "./ontology/ontology.ttl"
db = "./data/wiki_db_cleaned.csv"

g_rdf = Graph()
g_rdf.parse(rdf, format="turtle")
g_ontology = Graph()
g_ontology.parse(ontology, format="turtle")

#triples
rdf_triples = len(g_rdf)
ontology_triples = len(g_ontology)
total_triples = rdf_triples + ontology_triples

#subjects, objects, predicates
subjects = set(g_rdf.subjects())
objects = set(g_rdf.objects())
predicates = set(g_rdf.predicates())

#literals and resources
literals = set(o for o in objects if isinstance(o, str))
resources = objects - literals

#properties and classes
object_properties = set(g_ontology.subjects(RDF.type, OWL.ObjectProperty))
datatype_properties = set(g_ontology.subjects(RDF.type, OWL.DatatypeProperty))
properties = object_properties | datatype_properties
classes = set(g_ontology.subjects(RDF.type, OWL.Class)) | set(g_ontology.subjects(RDF.type, RDFS.Class))

#axioms
subclass_axioms = len(list(g_ontology.triples((None, RDFS.subClassOf, None))))
domain_axioms = len(list(g_ontology.triples((None, RDFS.domain, None))))
range_axioms = len(list(g_ontology.triples((None, RDFS.range, None))))

#sizes files
csv_size = os.path.getsize(db) / (1024 * 1024)
ttl_size = os.path.getsize(rdf) / (1024 * 1024)
onto_size = os.path.getsize(ontology) / (1024 * 1024)
rdf_total_size = ttl_size + onto_size

df = pd.read_csv(db)
l_df = len(df)

#size changes
changes_mb = rdf_total_size - csv_size
changes = (changes_mb / csv_size) * 100

print(f"Total triples: {total_triples}")
print(f"RDF triples: {rdf_triples}")
print(f"Ontology triples: {ontology_triples}")
print(f"Classes: {len(classes)}")
print(f"Properties: {len(properties)}")
print(f"Object properties: {len(object_properties)}")
print(f"Datatype properties: {len(datatype_properties)}")
print(f"Subjects: {len(subjects)}")
print(f"Objects: {len(objects)}")
print(f" - Literal values: {len(literals)}")
print(f" - Resource objects: {len(resources)}")
print(f"subClassOf axioms: {subclass_axioms}")
print(f"domain axioms: {domain_axioms}")
print(f"range axioms: {range_axioms}")

print("--------------------------------")
print(f"CSV size: {csv_size:.2f} MB")
print(f"RDF size: {ttl_size:.2f} MB")
print(f"Ontology size: {onto_size:.4f} MB")
print(f"Total RDF size: {rdf_total_size:.2f} MB")

print(f"CSV rows: {l_df}")
print(f"RDF triples: {rdf_triples}")

print(f"Change: {changes_mb:.2f} MB, {changes:.2f}%")