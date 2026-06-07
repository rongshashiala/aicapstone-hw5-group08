import rdflib
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
from pathlib import Path
import owlrl, os

ROOT = Path(__file__).parent.parent

CAP = Namespace("https://hcis.io/ontology/aicapstone/2026/")
G08 = Namespace("https://hcis.io/ontology/aicapstone/2026/group08/")

g = Graph()
g.parse(ROOT / "ontology" / "group-ontology.ttl", format="turtle")
print(f"Loaded {len(g)} triples (asserted)")

owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
print(f"After reasoning: {len(g)} triples (inferred)")

g.serialize(ROOT / "ontology" / "inferred-results-python.ttl", format="turtle")
print("Exported: inferred-results.ttl\n")

# ── Query 1: graspable_objects ───────────────────────────────────
q1 = """
PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/>
PREFIX g08: <https://hcis.io/ontology/aicapstone/2026/group08/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?obj ?label ?role WHERE {
    ?obj rdf:type g08:GraspableObject .
    OPTIONAL { ?obj cap:hasObjectLabel ?label . }
    OPTIONAL { ?obj cap:hasTaskRole    ?role  . }
} ORDER BY ?obj
"""
rows1 = list(g.query(q1))
print("="*65)
print("QUERY: graspable_objects  (inferred GraspableObject instances)")
print("="*65)
print(f"{'obj':<22} {'label':<22} {'role'}")
print("-"*65)
for r in rows1:
    obj   = str(r.obj).split("/")[-1]
    label = str(r.label) if r.label else "-"
    role  = str(r.role).split("/")[-1] if r.role else "-"
    print(f"{obj:<22} {label:<22} {role}")
print(f"\nTotal GraspableObject instances: {len(rows1)}")

# ── Query 2: task_objects (with Python-side flags) ───────────────
q2 = """
PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/>
PREFIX g08: <https://hcis.io/ontology/aicapstone/2026/group08/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?obj ?label ?color ?role WHERE {
    ?obj rdf:type ?objClass .
    ?objClass rdfs:subClassOf* cap:PhysicalObject .
    ?obj cap:hasTaskRole ?role .
    OPTIONAL { ?obj cap:hasObjectLabel ?label . }
    OPTIONAL { ?obj cap:hasColor       ?color . }
    FILTER(isIRI(?obj))
    FILTER(?obj != cap:TargetObject && ?obj != cap:ReferenceObject &&
           ?obj != cap:ContainerTarget && ?obj != cap:CollectableObject)
} ORDER BY ?role ?obj
"""

# Pre-compute inferred sets
graspable_set = {str(r.obj) for r in g.query(
    "SELECT ?obj WHERE { ?obj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://hcis.io/ontology/aicapstone/2026/group08/GraspableObject> . }")}
colorsort_set = {str(r.obj) for r in g.query(
    "SELECT ?obj WHERE { ?obj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://hcis.io/ontology/aicapstone/2026/group08/ColorSortableObject> . }")}

rows2 = list(g.query(q2))
print("\n" + "="*100)
print("QUERY: task_objects  (all task-relevant objects with inferred flags)")
print("="*100)
hdr = f"{'obj':<22} {'label':<22} {'color':<8} {'role':<22} {'GraspableObj':<14} {'ColorSortableObj'}"
print(hdr)
print("-"*100)
seen = set()
for r in rows2:
    key = str(r.obj)
    if key in seen: continue
    seen.add(key)
    obj   = key.split("/")[-1]
    label = str(r.label) if r.label else "-"
    color = str(r.color) if r.color else "-"
    role  = str(r.role).split("/")[-1] if r.role else "-"
    gras  = "true" if key in graspable_set  else "false"
    csort = "true" if key in colorsort_set  else "false"
    print(f"{obj:<22} {label:<22} {color:<8} {role:<22} {gras:<14} {csort}")
print(f"\nTotal task object instances: {len(seen)}")

# ── Save outputs ─────────────────────────────────────────────────
os.makedirs(ROOT / "results", exist_ok=True)

with open(ROOT / "results" / "graspable_objects_output.txt", "w") as f:
    f.write("QUERY: graspable_objects\n")
    f.write("Reasoner: owlrl (OWL RL / RDF(S) closure)\n")
    f.write("="*65 + "\n")
    f.write(f"{'obj':<22} {'label':<22} {'role'}\n")
    f.write("-"*65 + "\n")
    for r in rows1:
        obj   = str(r.obj).split("/")[-1]
        label = str(r.label) if r.label else "-"
        role  = str(r.role).split("/")[-1] if r.role else "-"
        f.write(f"{obj:<22} {label:<22} {role}\n")
    f.write(f"\nTotal inferred GraspableObject instances: {len(rows1)}\n")

with open(ROOT / "results" / "task_objects_output.txt", "w") as f:
    f.write("QUERY: task_objects\n")
    f.write("Reasoner: owlrl (OWL RL / RDF(S) closure)\n")
    f.write("="*100 + "\n")
    f.write(f"{'obj':<22} {'label':<22} {'color':<8} {'role':<22} {'GraspableObj':<14} {'ColorSortableObj'}\n")
    f.write("-"*100 + "\n")
    seen2 = set()
    for r in rows2:
        key = str(r.obj)
        if key in seen2: continue
        seen2.add(key)
        obj   = key.split("/")[-1]
        label = str(r.label) if r.label else "-"
        color = str(r.color) if r.color else "-"
        role  = str(r.role).split("/")[-1] if r.role else "-"
        gras  = "true" if key in graspable_set else "false"
        csort = "true" if key in colorsort_set else "false"
        f.write(f"{obj:<22} {label:<22} {color:<8} {role:<22} {gras:<14} {csort}\n")
    f.write(f"\nTotal task object instances: {len(seen2)}\n")

print("\nSaved: results/graspable_objects_output.txt")
print("Saved: results/task_objects_output.txt")
