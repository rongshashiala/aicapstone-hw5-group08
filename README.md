# HW5 Ontology Modeling for Physical AI

## 1. Project Title and Group Members

**Project Title:**
Ontology-Based Semantic Modeling and Reasoning for Physical AI Tasks

**Group:** Group 08

**Members:**

* 谷世蕊 111550189
* 葉莉莎 111550205
* 歐力思 111550202
* 劉培錦 111550193
* 林晶晶 111550190
* 李士平 110550049

---

## 2. Selected Tasks

### Baseline Task

**Toy-Block Collection**

The robot collects toy blocks scattered on a table and places them into a basket.

### Advanced Task

**Color-Sorting Toy-Block Collection**

The environment contains three toy blocks (red, blue, and green) and three baskets with matching colors. The robot must place each block into the basket with the corresponding color.

---

## 3. Ontology Design

The ontology is based on the course-affordance.ttl provided by the instructor.

For the baseline task, the ontology models:

* Toy blocks
* Baskets
* Physical objects
* Task roles
* Affordances

The ontology uses OWL reasoning to infer whether an object is graspable.

For the advanced task, the ontology extends the baseline ontology by introducing:

* `g08:ColorSortingAffordance`
* `g08:ColorSortableObject`
* `g08:ColorSortingBasket`

`ColorSortingBasket` is defined as a subclass of `cap:Basket` and represents baskets used in the color-sorting task.

Objects participating in color sorting are associated with the color-sorting affordance. OWL reasoning is then used to infer membership in the `ColorSortableObject` class.

---

## 4. Modeled Objects and Affordances

| Object           | Class              | Affordances                                   |
| ---------------- | ------------------ | --------------------------------------------- |
| redBlock01       | ToyBlock           | GraspingAffordance, ColorSortingAffordance    |
| blueBlock01      | ToyBlock           | GraspingAffordance, ColorSortingAffordance    |
| greenBlock01     | ToyBlock           | GraspingAffordance, ColorSortingAffordance    |
| baselineBasket01 | Basket             | ContainmentAffordance                         |
| redBasket01      | ColorSortingBasket | ContainmentAffordance, ColorSortingAffordance |
| blueBasket01     | ColorSortingBasket | ContainmentAffordance, ColorSortingAffordance |
| greenBasket01    | ColorSortingBasket | ContainmentAffordance, ColorSortingAffordance |
| blueCup01        | Cup                | GraspingAffordance, StackabilityAffordance    |
| pinkCup01        | Cup                | GraspingAffordance, StackabilityAffordance    |
| fork01           | Fork               | GraspingAffordance                            |
| knife01          | Knife              | GraspingAffordance                            |
| plate01          | Plate              | SupportAffordance                             |

---

## 5. Namespace Policy

The ontology follows the namespace policy required by the course.

### Course Namespace

Used for instructor-provided ontology terms:

```ttl
cap: <https://hcis.io/ontology/aicapstone/2026/>
```

Examples:

* cap:ToyBlock
* cap:Basket
* cap:GraspingAffordance
* cap:TaskRole

### Group Namespace

Used for group-specific extensions and all group-defined instances:

```ttl
g08: <https://hcis.io/ontology/aicapstone/2026/group08/>
```

Examples:

* g08:GraspableObject
* g08:ColorSortingAffordance
* g08:ColorSortableObject
* g08:ColorSortingBasket
* g08:blueBlock01

**Note on GraspableObject**: In our implementation, GraspableObject was intentionally assigned to the local group namespace (g08:GraspableObject) rather than the cap: prefix. This design choice was maintained throughout the development pipeline to preserve the integrity of our generated graphs and query results.

---

## 6. Instructions for Running the Query

1. Open Protégé (5.6.9).
2. Load the ontology file.
3. Start the HermiT reasoner.
4. Execute the SPARQL query provided in the query file.
5. View the inferred query results.

---

## 7. Expected Query Output

### Graspable Object Query

Example inferred results:

```text
blueCup01
pinkCup01
fork01
knife01
redBlock01
blueBlock01
greenBlock01
```

### Color-Sortable Object Query

Example inferred results:

```text
redBlock01
blueBlock01
greenBlock01
redBasket01
blueBasket01
greenBasket01
```

---

## 8. What Is Inferred Rather Than Asserted

The ontology does not manually assert inferred classes.

For example:

```ttl
redBlock01 a cap:ToyBlock .
```

is explicitly asserted.

The following statement is inferred by the reasoner:

```ttl
redBlock01 a g08:GraspableObject .
```

because `ToyBlock` has a `GraspingAffordance`, and `GraspableObject` is defined using an OWL equivalent class restriction.

Similarly,

```ttl
redBlock01 a g08:ColorSortableObject .
```

and

```ttl
redBasket01 a g08:ColorSortableObject .
```

are inferred through the `ColorSortingAffordance` definition rather than manually asserted.

---

## 9. Generation of inferred-results-protege.ttl

The inferred ontology was generated using Protégé and the HermiT reasoner.

Procedure:

1. Start the HermiT reasoner.
2. Verify inferred class memberships.
3. Select:

```
Reasoner → Export inferred axioms as ontology
```

4. Include:

* Subclasses
* Equivalent Classes
* Class Assertions

5. Include:

* Annotations
* Asserted Logical Axioms

6. Save the exported ontology as:

```
ontology/inferred-results.ttl
```
7. For better readability, open the newly saved inferred-results.ttl in Protégé, add the prefixes for cap and g08, then save and close the file.

---

## 10. Project Files

Please refer to report.pdf for further details

| File                                    | Description                          |
| --------------------------------------- | ------------------------------------ |
| ontology/group-ontology.ttl             | Main ontology                        |
| ontology/inferred-results-protere.ttl           | Ontology with inferred axioms from protege       |
| ontology/inferred-results-python.ttl           | Ontology with inferred axioms from run_reasoning.py       |
| doc/widoco/doc | contents of widoco
| queries/graspable_object.rq             | Query: all GraspableObjects          |
| queries/color_sortable_objects.rq       | Query: all ColorSortableObjects      |
| queries/task_objects.rq                 | Query all task objects in python pipeline |
| results/...                             | Query output and screenshots         |
| src/run_reasoning.py | python pipeline work |
| README.md                               | Project documentation                |
| report.pdf                               | Project report                |