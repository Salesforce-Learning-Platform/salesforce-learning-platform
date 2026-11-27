# 🧩 Decomposition

## Splitting Without Losing

Normalizing means **decomposing** a table into smaller ones, and a decomposition is only acceptable if the original information can be rebuilt. A decomposition is a **lossless join** (or non-additive) decomposition if, for every relation that satisfies the dependencies, joining its projections gives back exactly the original ([Wikipedia: Lossless join decomposition](https://en.wikipedia.org/wiki/Lossless_join_decomposition)). "Lossy" is a slightly misleading name: no rows disappear, but **extra** rows appear, and the true ones can no longer be told apart from the false ones. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54; the results are deterministic.

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE appointments (patient TEXT, doctor TEXT, slot TEXT)")
db.executemany("INSERT INTO appointments VALUES (?, ?, ?)", [("p1", "d1", "09:00"), ("p2", "d1", "10:00")])
db.execute("CREATE TABLE who_sees AS SELECT DISTINCT patient, doctor FROM appointments")
db.execute("CREATE TABLE doctor_hours AS SELECT DISTINCT doctor, slot FROM appointments")
print("original:", db.execute("SELECT * FROM appointments ORDER BY patient, slot").fetchall())
print("rejoined:", db.execute("SELECT patient, doctor, slot FROM who_sees NATURAL JOIN doctor_hours ORDER BY patient, slot").fetchall())
db.close()
```

```text
original: [('p1', 'd1', '09:00'), ('p2', 'd1', '10:00')]
rejoined: [('p1', 'd1', '09:00'), ('p1', 'd1', '10:00'), ('p2', 'd1', '09:00'), ('p2', 'd1', '10:00')]
```

The join invents two appointments that never happened. The split cut apart the connection between a patient and a time.

## 📐 When Is a Split Safe?

For a split into two parts there is a simple criterion: the decomposition of R into R₁ and R₂ is lossless exactly when the shared attributes determine all of one side: (R₁ ∩ R₂) → (R₁ − R₂) or (R₁ ∩ R₂) → (R₂ − R₁) follows from the dependencies ([Wikipedia: Lossless join decomposition](https://en.wikipedia.org/wiki/Lossless_join_decomposition)). One direction is **Heath's theorem**: if R satisfies X → Y, then R equals the join of its projections onto XY and onto X with the remaining attributes ([Wikipedia: Functional dependency](https://en.wikipedia.org/wiki/Functional_dependency)). In the experiment above, the shared attribute, `doctor`, determines neither the patient nor the slot.

For any number of parts there is the **chase**, a fixed-point algorithm for reasoning about data dependencies ([Wikipedia: Chase](https://en.wikipedia.org/wiki/Chase_(algorithm))). To test a decomposition, it builds a table with one row per part: the row has a "known" symbol for each attribute of its part and a unique unknown symbol elsewhere. Whenever two rows agree on the left side of a dependency, their right-side symbols are made equal, with known symbols winning. The decomposition is lossless exactly when some row ends up completely known:

```python
from itertools import combinations

def fd(text):
    """fd("a b -> c") means: a and b together determine c."""
    left, right = text.split("->")
    return frozenset(left.split()), frozenset(right.split())

def show(attributes):
    return " ".join(sorted(attributes))

CLINIC = frozenset("patient name phone doctor dr_name specialty room fee slot".split())
CLINIC_FDS = [
    fd("patient -> name phone"),                # each patient has one name and phone number
    fd("doctor -> dr_name specialty room"),     # each doctor has one name, specialty, and room
    fd("specialty -> fee"),                     # the fee depends only on the specialty
    fd("patient slot -> doctor"),               # a patient sees one doctor in a time slot
    fd("doctor slot -> patient"),               # a doctor sees one patient in a time slot
]

def closure(attributes, fds):
    """All attributes determined by `attributes`: keep applying dependencies until nothing new appears."""
    result = set(attributes)
    changed = True
    while changed:
        changed = False
        for left, right in fds:
            if left <= result and not right <= result:
                result |= right
                changed = True
    return frozenset(result)

def candidate_keys(schema, fds):
    """The minimal sets of attributes whose closure is the whole schema."""
    keys = []
    for size in range(1, len(schema) + 1):
        for chosen in combinations(sorted(schema), size):
            chosen = frozenset(chosen)
            if not any(key <= chosen for key in keys) and closure(chosen, fds) >= schema:
                keys.append(chosen)
    return keys

def chase_is_lossless(schema, parts, fds):
    rows = [{a: ("known", a) if a in part else ("unknown", i, a) for a in schema} for i, part in enumerate(parts)]
    changed = True
    while changed:
        changed = False
        for left, right in fds:
            for first in rows:
                for second in rows:
                    if first is not second and all(first[a] == second[a] for a in left):
                        for a in right:
                            if first[a] != second[a]:
                                keep, drop = sorted([first[a], second[a]])      # "known" sorts before "unknown"
                                for row in rows:
                                    if row[a] == drop:
                                        row[a] = keep
                                changed = True
    return any(all(row[a] == ("known", a) for a in schema) for row in rows)

VISITS = frozenset({"patient", "slot", "doctor", "room"})
VISIT_FDS = [fd("patient slot -> doctor"), fd("doctor -> room")]
for first, second in (("patient slot doctor", "doctor room"), ("patient slot room", "doctor room")):
    parts = [frozenset(first.split()), frozenset(second.split())]
    print(" + ".join("{" + show(p) + "}" for p in parts), "lossless:", chase_is_lossless(VISITS, parts, VISIT_FDS))
DESIGN = [frozenset(p.split()) for p in ("patient name phone", "doctor dr_name specialty room", "specialty fee", "patient slot doctor")]
print("the four clinic tables are lossless:", chase_is_lossless(CLINIC, DESIGN, CLINIC_FDS))
```

```text
{doctor patient slot} + {doctor room} lossless: True
{patient room slot} + {doctor room} lossless: False
the four clinic tables are lossless: True
```

## 🛠️ Building a 3NF Design: Synthesis

A decomposition into 3NF that is both lossless and **dependency preserving** (every original dependency can still be checked from the dependencies inside the parts) always exists and can be computed in polynomial time ([Wikipedia: Third normal form](https://en.wikipedia.org/wiki/Third_normal_form)). The standard **synthesis** method starts from a minimal cover: make one table for each dependency in the cover, holding its left and right sides; if no table contains a candidate key of the whole schema, add one that does; and drop any table contained in another:

```python
def minimal_cover(fds):
    """A small equivalent set of dependencies: no extra attributes, no redundant dependencies."""
    # 1. one attribute on each right side
    working = [(left, frozenset([a])) for left, right in fds for a in sorted(right - left)]
    # 2. drop attributes that a left side does not need
    for i, (left, right) in enumerate(working):
        for a in sorted(left):
            smaller = working[i][0] - {a}
            if smaller and right <= closure(smaller, working):
                working[i] = (smaller, right)
    # 3. drop dependencies that follow from the others
    kept = list(dict.fromkeys(working))
    for dependency in list(kept):
        others = [d for d in kept if d != dependency]
        if dependency[1] <= closure(dependency[0], others):
            kept = others
    # 4. merge dependencies with the same left side
    merged = {}
    for left, right in kept:
        merged[left] = merged.get(left, frozenset()) | right
    return list(merged.items())

def synthesize_3nf(schema, fds):
    parts = [left | right for left, right in minimal_cover(fds)]
    keys = candidate_keys(schema, fds)
    if not any(key <= part for part in parts for key in keys):
        parts.append(keys[0])                                    # keep the tables connected through a key
    parts = list(dict.fromkeys(parts))
    return [p for p in parts if not any(p < other for other in parts)]

for part in synthesize_3nf(CLINIC, CLINIC_FDS):
    print("  ", show(part))
```

```text
   name patient phone
   doctor dr_name room specialty
   fee specialty
   doctor patient slot
```

Without being told anything but the five dependencies, the algorithm produces the same four tables that the previous lesson designed by hand.

## ✂️ Building a BCNF Design: Decomposition

To reach BCNF, repeatedly split a table that violates it: if X → Y violates BCNF in a table R, replace R by two tables, one with X⁺ (everything X determines in R) and one with X and the rest, and repeat on each ([Wikipedia: Boyce-Codd normal form](https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form)). Each split is lossless by the criterion above:

```python
def bcnf_violation(table, fds):
    for size in range(1, len(table)):
        for chosen in combinations(sorted(table), size):
            left = frozenset(chosen)
            determined = closure(left, fds) & table
            if determined != left and determined != table:         # X -> something, but X is not a superkey of R
                return left
    return None

def decompose_bcnf(table, fds):
    left = bcnf_violation(table, fds)
    if left is None:
        return [table]
    first = closure(left, fds) & table
    return decompose_bcnf(first, fds) + decompose_bcnf((table - first) | left, fds)

TEACHING = frozenset({"student", "course", "instructor"})
TEACHING_FDS = [fd("student course -> instructor"), fd("instructor -> course")]
for name, schema, fds in (("clinic", CLINIC, CLINIC_FDS), ("teaching", TEACHING, TEACHING_FDS)):
    for method, design in (("3NF synthesis", synthesize_3nf(schema, fds)), ("BCNF decomposition", decompose_bcnf(schema, fds))):
        print(f"{name:<9} {method:<19} " + " | ".join(show(p) for p in design),
              f"(lossless: {chase_is_lossless(schema, design, fds)})")
```

```text
clinic    3NF synthesis       name patient phone | doctor dr_name room specialty | fee specialty | doctor patient slot (lossless: True)
clinic    BCNF decomposition  fee specialty | doctor dr_name room specialty | name patient phone | doctor patient slot (lossless: True)
teaching  3NF synthesis       course instructor student (lossless: True)
teaching  BCNF decomposition  course instructor | instructor student (lossless: True)
```

For the clinic both methods give the same tables. For the teaching example they differ: 3NF keeps one table, while BCNF splits it into (instructor, course) and (instructor, student). That split removes the redundancy, and it is lossless, but it loses something: **no single table holds student, course, and instructor together**, so the rule "a student has one instructor per course" cannot be enforced by keys on the new tables. This cannot always be avoided: Beeri and Bernstein showed in 1979 that dependencies of the shape {AB → C, C → B} cannot be represented by a BCNF schema that preserves them ([Wikipedia: Boyce-Codd normal form](https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form)). The loss is real:

```python
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE teaches (instructor TEXT PRIMARY KEY, course TEXT NOT NULL)")      # instructor -> course
db.execute("CREATE TABLE studies (student TEXT, instructor TEXT, PRIMARY KEY (student, instructor))")
db.executemany("INSERT INTO teaches VALUES (?, ?)", [("hopper", "databases"), ("noether", "databases")])
db.executemany("INSERT INTO studies VALUES (?, ?)", [("ada", "hopper"), ("ada", "noether")])      # both accepted
print(db.execute("""SELECT student, course, count(DISTINCT instructor) AS instructors
                    FROM studies NATURAL JOIN teaches GROUP BY student, course""").fetchall())
db.close()
```

```text
[('ada', 'databases', 2)]
```

Every key of the new tables is satisfied, yet Ada now has two instructors for databases. Enforcing the rule needs a trigger, an application check, or keeping the 3NF table and accepting its redundancy. So the practical advice is: aim for BCNF; where BCNF would lose a dependency that matters, 3NF is a reasonable stopping point.

## ✅ Checking the Code

On 1,500 random sets of dependencies with random decompositions, every decomposition that the chase called lossless rebuilt 30 random relations satisfying the dependencies exactly (1,214 cases), every one that it called lossy had its final chase table as a concrete counterexample (286 cases), and the two-part criterion agreed with the chase in all 658 two-part cases. On the same sets, `synthesize_3nf` was always lossless, dependency preserving, and in 3NF, and `decompose_bcnf` was always lossless and in BCNF, although it lost a dependency in 187 cases.

## Common Misconceptions

- **"Lossy means rows are lost."** The rejoined table has extra, false rows; the information about which are true is what is lost.
- **"Any split that shares a column is safe."** The shared attributes must determine one of the two sides.
- **"BCNF is always better than 3NF."** BCNF can make a dependency impossible to enforce with keys.
- **"Decomposition must be done by intuition."** The synthesis and decomposition algorithms turn dependencies into designs mechanically; judgement is still needed to state the right dependencies.

## ➡️ Next

This completes the Normalisation module: dependencies, the normal forms, and how to decompose tables safely. The next module of this section, Transactions and ACID, turns from how data is arranged to how changes to it stay correct while many operations run at once and when failures happen.
