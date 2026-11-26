# 🧷 Functional Dependencies

## What a Functional Dependency Says

Normalization is built on one idea. A **functional dependency** X → Y between two sets of attributes says that rows with the same values of X always have the same values of Y: X **determines** Y. Equivalently, the projection of the relation onto X and Y is a function. A dependency whose right side is part of its left side, such as {patient, slot} → {patient}, is **trivial** ([Wikipedia: Functional dependency](https://en.wikipedia.org/wiki/Functional_dependency)). Dependencies are rules about the business, such as "each doctor has one room". Like keys ([relations-and-keys.md](../the-relational-model/relations-and-keys.md)), they must hold in every valid state; a table's current rows can only show that a dependency does **not** hold.

The lessons of this module use one realistic schema, a clinic's appointment sheet with nine attributes, kept in one wide table: the patient (`patient`, `name`, `phone`), the doctor (`doctor`, `dr_name`, `specialty`, `room`), the specialty's `fee`, and the time `slot`. The practical introduction to the normal forms is [normalization.md](../../../backend/database-design-and-modeling/normalization.md); this module supplies the theory behind it. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); every result is deterministic.

```python
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

def holds(rows, left, right):
    """Do these rows satisfy left -> right? (Rows are dictionaries.)"""
    seen = {}
    for row in rows:
        key = tuple(row[a] for a in sorted(left))
        value = tuple(row[a] for a in sorted(right))
        if seen.setdefault(key, value) != value:
            return False
    return True

rows = [{"doctor": "d1", "room": "R1", "slot": "09:00"},
        {"doctor": "d1", "room": "R1", "slot": "10:00"},
        {"doctor": "d2", "room": "R1", "slot": "11:00"}]
for text in ("doctor -> room", "room -> doctor", "slot -> doctor"):
    print(f"{text:<18} holds in these rows: {holds(rows, *fd(text))}")
```

```text
doctor -> room     holds in these rows: True
room -> doctor     holds in these rows: False
slot -> doctor     holds in these rows: True
```

The rows refute `room → doctor` (room R1 has two doctors). They do not refute `slot → doctor`, but that proves nothing: another day, two doctors will work at the same time.

## ⚙️ Reasoning About Dependencies: Armstrong's Axioms

From some dependencies others follow. **Armstrong's axioms** (1974) are three inference rules that are both **sound** (they produce only dependencies that really follow) and **complete** (applied repeatedly, they produce every dependency that follows) ([Wikipedia: Armstrong's axioms](https://en.wikipedia.org/wiki/Armstrong%27s_axioms)):

| Axiom | Rule |
|-------|------|
| **Reflexivity** | if Y ⊆ X, then X → Y |
| **Augmentation** | if X → Y, then XZ → YZ |
| **Transitivity** | if X → Y and Y → Z, then X → Z |

Useful rules follow from them: **union** (X → Y and X → Z give X → YZ), **decomposition** (X → YZ gives X → Y and X → Z), and **pseudotransitivity** (X → Y and WY → Z give WX → Z) (the same article). For example, union: augment X → Y with X to get X → XY; augment X → Z with Y to get XY → YZ; then transitivity gives X → YZ.

## 🔁 The Closure of a Set of Attributes

In practice one does not apply the axioms by hand. The **closure** X⁺ of a set of attributes X is the set of all attributes that X determines ([Wikipedia: Functional dependency](https://en.wikipedia.org/wiki/Functional_dependency)), and it is easy to compute: start with X and keep adding the right side of any dependency whose left side is already inside. Then X → Y follows from the dependencies exactly when Y ⊆ X⁺, and X is a **superkey** exactly when X⁺ is the whole schema:

```python
from itertools import combinations

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

for attributes in ({"specialty"}, {"doctor"}, {"patient", "slot"}):
    print(f"closure of {{{show(attributes)}}}:".ljust(32), show(closure(attributes, CLINIC_FDS)))
print("candidate keys:", " | ".join("{" + show(key) + "}" for key in candidate_keys(CLINIC, CLINIC_FDS)))
```

```text
closure of {specialty}:          fee specialty
closure of {doctor}:             doctor dr_name fee room specialty
closure of {patient slot}:       doctor dr_name fee name patient phone room slot specialty
candidate keys: {doctor slot} | {patient slot}
```

The clinic has two candidate keys, {patient, slot} and {doctor, slot}: either identifies an appointment, because a patient or a doctor can be in only one appointment per slot. A shortcut helps with hand calculation: an attribute that appears on no right side cannot be derived, so it belongs to **every** candidate key; here that is `slot`.

## 🧹 Minimal (Canonical) Cover

Different sets of dependencies can say the same thing. A **minimal cover**, also called a canonical cover, is an equivalent set with no unnecessary attribute on any left side, no redundant dependency, and each left side appearing once; there can be several such covers for one set ([Wikipedia: Canonical cover](https://en.wikipedia.org/wiki/Canonical_cover)). It is the starting point for designing tables. The algorithm splits the right sides, removes unneeded left-side attributes, removes dependencies that follow from the rest, and merges equal left sides:

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

messy = CLINIC_FDS + [fd("patient slot -> doctor name"),        # name already follows from patient
                      fd("doctor specialty -> fee"),            # doctor is not needed: specialty -> fee
                      fd("doctor -> fee")]                      # follows: doctor -> specialty -> fee
print(len(messy), "dependencies in the messy set; a minimal cover:")
for left, right in minimal_cover(messy):
    print(f"   {show(left):<16} -> {show(right)}")
```

```text
8 dependencies in the messy set; a minimal cover:
   patient          -> name phone
   doctor           -> dr_name room specialty
   specialty        -> fee
   patient slot     -> doctor
   doctor slot      -> patient
```

The redundant additions disappear, and the cover is exactly the five rules that describe the clinic.

## ✅ Checking the Code

Each function was compared with a definition that uses none of the rules above. A dependency follows from a set exactly when every relation of **two rows** that satisfies the set also satisfies it, because a violation always involves just two rows, and any two rows of a relation that satisfies the set satisfy it too; so it can be tested by trying every set of attributes on which two rows could agree. On 1,500 random sets of dependencies over up to five attributes, `closure` and `candidate_keys` matched this definition for every set of attributes, and every minimal cover was equivalent to its original, had no removable attribute or dependency, and had distinct left sides.

## Common Misconceptions

- **"A dependency that holds in my data holds in general."** Data can refute a dependency, never prove it; dependencies come from the rules of the business.
- **"X → Y means Y → X."** A doctor determines a room, but a room can be shared by several doctors.
- **"A minimal cover is unique."** A set of dependencies can have several minimal covers; they are equivalent.
- **"Transitivity is the only rule you need."** Without augmentation and reflexivity, some dependencies that follow cannot be derived.

## ➡️ Next

Continue to [normal-forms.md](normal-forms.md): what first, second, third, and Boyce-Codd normal form require, tested on the clinic.
