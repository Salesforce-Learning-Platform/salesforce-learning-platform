# 📏 Normal Forms

## Why Normal Forms?

A table that mixes facts about different things stores some facts many times, which causes **update anomalies** (change one copy and not the others), **insertion anomalies** (a fact cannot be recorded until an unrelated one exists), and **deletion anomalies** (removing one fact removes another) ([normalization.md](../../../backend/database-design-and-modeling/normalization.md) shows each). The **normal forms** are tests, stated with the functional dependencies of the previous lesson ([functional-dependencies.md](functional-dependencies.md)), that say how much of this redundancy a table can still contain. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) with SQLite 3.54; the results are deterministic.

## 🪜 The Ladder

A **prime** attribute belongs to at least one candidate key; the others are **non-prime**.

| Form | Requirement |
|------|-------------|
| **1NF** | every field holds a single, atomic value, not a set of values or a nested table |
| **2NF** | 1NF, and no non-prime attribute depends on **part** of a candidate key (no partial dependency) |
| **3NF** | for every non-trivial dependency X → Y, either X is a superkey or every attribute of Y − X is prime |
| **BCNF** | for every non-trivial dependency X → Y, X is a superkey |

Codd defined 1NF, 2NF, and 3NF; his 3NF requires 2NF and that no non-prime attribute depend transitively on a candidate key, and the equivalent form in the table is Carlo Zaniolo's of 1982 ([Wikipedia: First normal form](https://en.wikipedia.org/wiki/First_normal_form), [Second](https://en.wikipedia.org/wiki/Second_normal_form), [Third](https://en.wikipedia.org/wiki/Third_normal_form)). **Boyce-Codd normal form (BCNF)** is slightly stricter than 3NF: it removes all redundancy that comes from functional dependencies, and every BCNF table is in 3NF ([Wikipedia: Boyce-Codd normal form](https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form)). A memorable way to read 2NF and 3NF, from William Kent, is that every non-key attribute should be a fact about the key, the whole key, and nothing but the key, applied to every candidate key.

## 🔍 Testing a Table

To test a table that is part of a larger design, we need the dependencies that hold **inside** it: for every subset X of its attributes, the attributes of the table that X determines. The following functions list the violations of each form:

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

def dependencies_within(table, fds):
    """Every X -> Y that follows from fds and stays inside the table (one pair per X)."""
    for size in range(1, len(table) + 1):
        for chosen in combinations(sorted(table), size):
            left = frozenset(chosen)
            right = (closure(left, fds) & table) - left
            if right:
                yield left, right

def normal_form(table, fds):
    """The highest of 1NF (assumed), 2NF, 3NF, and BCNF that the table satisfies, with one example violation."""
    keys = candidate_keys(table, fds)
    prime = frozenset().union(*keys)
    partial = [(left, right - prime) for left, right in dependencies_within(table, fds)
               if right - prime and any(left < key for key in keys)]
    third = [(left, right - prime) for left, right in dependencies_within(table, fds)
             if right - prime and not closure(left, fds) >= table]
    boyce_codd = [(left, right) for left, right in dependencies_within(table, fds) if not closure(left, fds) >= table]
    for level, violations in (("1NF", partial), ("2NF", third), ("3NF", boyce_codd)):
        if violations:
            left, right = violations[0]
            return level, f"{show(left)} -> {show(right)}"
    return "BCNF", None

level, why = normal_form(CLINIC, CLINIC_FDS)
print(f"the wide clinic table is only in {level}; for the next form, this violates it: {why}")
```

```text
the wide clinic table is only in 1NF; for the next form, this violates it: doctor -> dr_name fee room specialty
```

The wide table fails 2NF: `dr_name`, `room`, and `specialty` (and, through `specialty`, `fee`) depend on `doctor`, which is only **part** of the key {doctor, slot}, so they are repeated for every appointment of that doctor. In the same way the patient's details depend on part of {patient, slot}.

## 🏗️ Normalizing the Clinic

Splitting the table so that each rule gets a table of its own fixes the problem. The design below follows the dependencies: patient facts, doctor facts, the fee of each specialty, and the appointments. The function checks each part, and shows what happens if the specialty's fee is left in the doctor table:

```python
DESIGN = {
    "patients":     frozenset({"patient", "name", "phone"}),
    "doctors":      frozenset({"doctor", "dr_name", "specialty", "room"}),
    "specialties":  frozenset({"specialty", "fee"}),
    "appointments": frozenset({"patient", "slot", "doctor"}),
}
print(f"doctors with the fee kept inside: {normal_form(DESIGN['doctors'] | {'fee'}, CLINIC_FDS)}")
for name, table in DESIGN.items():
    keys = " | ".join("{" + show(key) + "}" for key in candidate_keys(table, CLINIC_FDS))
    print(f"{name:<13} {normal_form(table, CLINIC_FDS)[0]:<5} keys: {keys}")
```

```text
doctors with the fee kept inside: ('2NF', 'specialty -> fee')
patients      BCNF  keys: {patient}
doctors       BCNF  keys: {doctor}
specialties   BCNF  keys: {specialty}
appointments  BCNF  keys: {doctor slot} | {patient slot}
```

Keeping `fee` with the doctors would leave a **transitive** dependency, doctor → specialty → fee: the fee of a specialty would be stored once per doctor. That table is in 2NF but not 3NF. With the fee in its own table, all four tables are in BCNF.

## 🗄️ The Same Design in a Database

The next block fills one wide table with consistent appointments, splits it with `SELECT DISTINCT`, and joins the four parts back. Then it changes a doctor's room in both designs:

```python
import random
import sqlite3

generator = random.Random(11)
patients = {f"p{i}": (f"patient {i}", f"555-{i:04d}") for i in range(1, 7)}
fees = {"cardiology": 90, "dermatology": 60, "pediatrics": 50}
doctors = {f"d{i}": (f"dr {i}", generator.choice(sorted(fees)), f"R{i}") for i in range(1, 5)}
appointments = []
for slot in ("09:00", "10:00", "11:00", "12:00"):
    chosen_patients = generator.sample(sorted(patients), 3)
    chosen_doctors = generator.sample(sorted(doctors), 3)             # one patient per doctor per slot
    appointments += [(p, d, slot) for p, d in zip(chosen_patients, chosen_doctors)]

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE wide (patient, name, phone, doctor, dr_name, specialty, room, fee, slot)")
db.executemany("INSERT INTO wide VALUES (?,?,?,?,?,?,?,?,?)",
               [(p, *patients[p], d, *doctors[d], fees[doctors[d][1]], slot) for p, d, slot in appointments])
for name, table in DESIGN.items():
    db.execute(f"CREATE TABLE {name} AS SELECT DISTINCT {', '.join(sorted(table))} FROM wide")

columns = ", ".join(sorted(CLINIC))
original = sorted(db.execute(f"SELECT {columns} FROM wide"))
rejoined = sorted(db.execute(f"SELECT {columns} FROM appointments NATURAL JOIN patients NATURAL JOIN doctors NATURAL JOIN specialties"))
print(f"wide table: {len(original)} rows | rows after joining the four tables: {len(rejoined)} | identical: {rejoined == original}")

busiest = db.execute("SELECT doctor FROM wide GROUP BY doctor ORDER BY count(*) DESC, doctor LIMIT 1").fetchone()[0]
first_slot = db.execute("SELECT min(slot) FROM wide WHERE doctor = ?", (busiest,)).fetchone()[0]
db.execute("UPDATE wide SET room = 'R99' WHERE doctor = ? AND slot = ?", (busiest, first_slot))   # one row only
print(f"wide design, after updating one appointment: {busiest} now has rooms",
      sorted({r for (r,) in db.execute("SELECT room FROM wide WHERE doctor = ?", (busiest,))}))
db.execute("UPDATE doctors SET room = 'R99' WHERE doctor = ?", (busiest,))                    # the fact lives once
print(f"normalized design: {busiest} has rooms", sorted({r for (r,) in db.execute(
    "SELECT room FROM appointments NATURAL JOIN doctors WHERE doctor = ?", (busiest,))}))
db.close()
```

```text
wide table: 12 rows | rows after joining the four tables: 12 | identical: True
wide design, after updating one appointment: d1 now has rooms ['R1', 'R99']
normalized design: d1 has rooms ['R99']
```

The four tables hold the same information as the wide one: joining them gives back exactly the original rows. The difference is that in the wide design one forgotten row leaves a doctor in two rooms at once, while in the normalized design the room is stored once and cannot disagree with itself.

## ⚖️ When 3NF Is Not BCNF

3NF and BCNF differ only when candidate keys **overlap**, and even then not always; a 3NF table without several overlapping candidate keys is in BCNF ([Wikipedia: Boyce-Codd normal form](https://en.wikipedia.org/wiki/Boyce%E2%80%93Codd_normal_form)). The classic example: students take courses with instructors; a student has one instructor for each course, and each instructor teaches only one course:

```python
TEACHING = frozenset({"student", "course", "instructor"})
TEACHING_FDS = [fd("student course -> instructor"), fd("instructor -> course")]
print("keys:", " | ".join("{" + show(key) + "}" for key in candidate_keys(TEACHING, TEACHING_FDS)))
print("normal form:", normal_form(TEACHING, TEACHING_FDS))
```

```text
keys: {course student} | {instructor student}
normal form: ('3NF', 'instructor -> course')
```

The table is in 3NF, because `course` is prime (it belongs to the key {student, course}), but it is not in BCNF, because `instructor` determines `course` without being a superkey: the instructor's course is repeated for every student. [decomposition.md](decomposition.md) shows what splitting it costs.

## ✅ Checking the Code

`normal_form` gave the same answer as the definitions applied directly with the two-row test of the previous lesson, on 1,500 random sets of dependencies over up to five attributes.

## Common Misconceptions

- **"Third normal form means no redundancy."** A 3NF table can still repeat facts when candidate keys overlap; BCNF removes the redundancy that functional dependencies cause.
- **"A table with a single-column primary key is automatically in 2NF."** 2NF is about every candidate key; a table with a composite candidate key besides its primary key can still have partial dependencies.
- **"Normal forms are about performance."** They are about storing each fact once so that the data cannot contradict itself.
- **"More normalized is always better."** Reads need more joins; deliberate denormalization is sometimes right ([normalization.md](../../../backend/database-design-and-modeling/normalization.md)).

## ➡️ Next

Continue to [decomposition.md](decomposition.md): how to split tables without losing information, the algorithms that build 3NF and BCNF designs, and what BCNF can cost.
