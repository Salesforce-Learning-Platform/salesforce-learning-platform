# 🧩 File Allocation

## Which Blocks Hold the File?

[file-system-basics.md](file-system-basics.md) showed that a file is a *mapping* from offsets to blocks. This file asks how that mapping is built: when a program creates a file of *n* blocks, which free blocks does the file system give it, and how does it remember them? The problem is the one of [memory-allocation.md](../memory-management/memory-allocation.md) in a new setting, with a new set of criteria. A good method should use the disk's space well (little wasted to fragmentation), allow quick **random access** (jump to byte 5,000,000 without reading everything before it), let files **grow**, keep the bookkeeping **small**, and survive damage. Three classic methods trade these off differently: **contiguous**, **linked**, and **indexed** allocation. A fourth, **extents**, which combines the strengths of the first and the third, is what most modern file systems use.

This file builds each method as a small class on a simulated disk, compares them on the same scenario, measures what it costs to reach a block, computes how large a file the Unix inode scheme can describe, and runs an experiment on a nearly full disk. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); every result is deterministic.

## 🧮 Four Allocators on a Simulated Disk

The classes below share a `Disk` of numbered blocks that remembers which file owns each block. Each subclass supplies the policy for `create`, and a `reads_to_reach` method that counts how many disk blocks must be *read* to find the data block with a given number in a file (assuming nothing is cached, except that the file's inode is already in memory):

```python
class Disk:
    """A disk of numbered blocks. Each allocation method decides which free blocks a new file receives."""

    def __init__(self, size):
        self.size = size
        self.owner = [None] * size                      # which file owns each block (None means free)
        self.files = {}                                 # file name -> its blocks, in file order

    def free_blocks(self):
        return [b for b in range(self.size) if self.owner[b] is None]

    def delete(self, name):
        for block in self.files.pop(name):
            self.owner[block] = None

    def _give(self, name, blocks):
        for block in blocks:
            self.owner[block] = name
        self.files[name] = list(blocks)
        return list(blocks)

    def map(self):
        return "".join(owner or "." for owner in self.owner)


class ContiguousDisk(Disk):
    """Contiguous allocation: a file is one run of consecutive blocks, so the directory needs only (start, length)."""

    def create(self, name, count):
        run = 0
        for block in range(self.size):
            run = run + 1 if self.owner[block] is None else 0
            if run == count:                            # first fit: the first run of free blocks that is long enough
                return self._give(name, range(block - count + 1, block + 1))
        return None                                      # enough blocks may be free in total, but not in one run

    def reads_to_reach(self, name, index):
        return 1                                         # start + index is the address: one read


class LinkedDisk(Disk):
    """Linked allocation: any free blocks; each block holds the number of the next block of the same file."""

    def create(self, name, count):
        free = self.free_blocks()[:count]
        if len(free) < count:
            return None
        return self._give(name, free)

    def reads_to_reach(self, name, index):
        return index + 1                                 # the chain must be followed from the first block


class IndexedDisk(Disk):
    """Indexed allocation, Unix style: 12 direct pointers in the inode, then a single, a double and a triple indirect block."""

    DIRECT = 12

    def __init__(self, size, block_bytes=4096, pointer_bytes=4):
        super().__init__(size)
        self.pointers_per_block = block_bytes // pointer_bytes

    def create(self, name, count):
        free = self.free_blocks()[:count]
        if len(free) < count:
            return None
        return self._give(name, free)

    def reads_to_reach(self, name, index):
        p = self.pointers_per_block
        if index < self.DIRECT:
            return 1                                     # the inode points straight at the data block
        index -= self.DIRECT
        for levels in (1, 2, 3):                         # single, double, triple indirect
            if index < p ** levels:
                return 1 + levels                        # one read per indirect block on the way, then the data block
            index -= p ** levels
        raise ValueError("beyond the largest file this inode can describe")

    def max_blocks(self):
        p = self.pointers_per_block
        return self.DIRECT + p + p ** 2 + p ** 3


def extents(blocks):
    """Describe a list of block numbers as (start, length) runs."""
    runs = []
    for block in blocks:
        if runs and block == runs[-1][0] + runs[-1][1]:
            runs[-1][1] += 1
        else:
            runs.append([block, 1])
    return [tuple(run) for run in runs]
```

## 🆚 The Same Scenario, Three Methods

A 24-block disk is filled with five files (A, B, C, D, F), and then B and D are deleted, leaving two holes of four blocks each. A new file E needs six blocks. Eight blocks are free in total, but not together:

```python
for kind in (ContiguousDisk, LinkedDisk, IndexedDisk):
    disk = kind(24)
    for name, count in (("A", 6), ("B", 4), ("C", 6), ("D", 4), ("F", 4)):
        disk.create(name, count)
    disk.delete("B")
    disk.delete("D")
    placed = disk.create("E", 6)
    print(f"{kind.__name__:>15}: {disk.map()}  free blocks left: {len(disk.free_blocks())}")
    print(f"{'':>15}  E placed: {placed is not None}" + (f", in the pieces {extents(placed)}" if placed else ", although 8 blocks are free"))
```

```text
 ContiguousDisk: AAAAAA....CCCCCC....FFFF  free blocks left: 8
                 E placed: False, although 8 blocks are free
     LinkedDisk: AAAAAAEEEECCCCCCEE..FFFF  free blocks left: 2
                 E placed: True, in the pieces [(6, 4), (16, 2)]
    IndexedDisk: AAAAAAEEEECCCCCCEE..FFFF  free blocks left: 2
                 E placed: True, in the pieces [(6, 4), (16, 2)]
```

Each letter in the map shows which file owns a block, and a dot is a free block. Contiguous allocation fails: the free space is split into two holes of four, and the new file needs a run of six. This is the external fragmentation of [memory-allocation.md](../memory-management/memory-allocation.md), and the cure is the same, either moving files around to make room (defragmentation) or not requiring contiguity. The other two methods do not: E takes the four blocks of one hole and two of the other, in two pieces, and the disk is used almost completely. The price of scattering shows up in what it costs to *find* a block.

## 🔎 Reaching Block *i* of a File

Contiguous allocation needs only the address of the first block and the length: block *i* is at *start + i*, one read. **Linked allocation** stores the number of the next block inside each block, so the directory holds just the first block, files can grow without limit, and no space is wasted to fragmentation, but reaching block *i* means following *i* pointers, one disk read each; it is a linked list on disk. **Indexed allocation** keeps all of a file's block addresses in an index, so any block can be found directly. The Unix inode keeps the index in the inode itself and grows it as needed: the first 12 addresses are direct pointers to data blocks, followed by one pointer to a *single indirect block* (a block full of further pointers), one to a *double indirect block* (pointers to single indirect blocks), and one to a *triple indirect block*. The levels of indirection say how many pointers must be followed before the data is reached, and the indirect blocks are allocated only as needed: a 12-block file is described by the inode alone, and a 13-block file needs one indirect block ([Wikipedia: Inode pointer structure](https://en.wikipedia.org/wiki/Inode_pointer_structure)). With 4,096-byte blocks and 4-byte pointers, an indirect block holds 1,024 of them. Here is the cost of reaching various blocks of a very large file:

```python
indexed = IndexedDisk(10)
print(f"{'block number':>12} | {'contiguous':>10} | {'linked':>9} | {'indexed':>7}")
for index in (0, 11, 12, 500, 1035, 1036, 5000, 1_000_000):
    print(f"{index:>12,} | {1:>10} | {index + 1:>9,} | {indexed.reads_to_reach('any', index):>7}")
```

```text
block number | contiguous |    linked | indexed
           0 |          1 |         1 |       1
          11 |          1 |        12 |       1
          12 |          1 |        13 |       2
         500 |          1 |       501 |       2
       1,035 |          1 |     1,036 |       2
       1,036 |          1 |     1,037 |       3
       5,000 |          1 |     5,001 |       3
   1,000,000 |          1 | 1,000,001 |       3
```

Linked allocation is cheap for sequential reading and hopeless for random access: block 1,000,000 would take a million reads. The index keeps the cost at one to four reads whatever the position, because the number of levels needed grows only logarithmically (every extra level multiplies the reach by 1,024). Block 11 is direct; blocks 12 to 1,035 need one indirect block; the next 1,048,576 blocks need two levels; and so on. The same structure lets the file system place data blocks anywhere on the disk, and it also makes it easy to locate the data at any position, since the block size is fixed.

## 📏 How Large a File Can an Inode Describe?

The number of blocks reachable is 12 + *p* + *p*<sup>2</sup> + *p*<sup>3</sup>, where *p* is the number of pointers in an indirect block, the block size divided by the pointer size (for example, 512-byte blocks and 4-byte pointers give 128 pointers per indirect block, as Wikipedia's article points out). The next block evaluates the formula for two block sizes:

```python
def human(n):
    for unit in ("bytes", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024 or unit == "TiB":
            return f"{n:,.1f} {unit}" if n != int(n) else f"{n:,.0f} {unit}"
        n /= 1024

print(f"{'block size':>10} | {'pointers per block':>18} | {'direct only':>11} | {'+ single':>10} | {'+ double':>10} | {'+ triple (maximum)':>20}")
for block in (1024, 4096):
    p = block // 4
    sizes = [12 * block, (12 + p) * block, (12 + p + p ** 2) * block, (12 + p + p ** 2 + p ** 3) * block]
    assert sizes[-1] == IndexedDisk(10, block, 4).max_blocks() * block
    print(f"{block:>10,} | {p:>18,} | {human(sizes[0]):>11} | {human(sizes[1]):>10} | {human(sizes[2]):>10} | {human(sizes[3]):>20}")
```

```text
block size | pointers per block | direct only |   + single |   + double |   + triple (maximum)
     1,024 |                256 |      12 KiB |    268 KiB |   64.3 MiB |             16.1 GiB
     4,096 |              1,024 |      48 KiB |    4.0 MiB |    4.0 GiB |              4.0 TiB
```

With 4 KiB blocks, direct pointers alone cover files of 48 KiB, which is enough for most files (so most files need no indirect block at all), and the triple-indirect level reaches about 4 TiB. This design is the Unix inode pointer structure of the Unix File System and of related file systems, including ext3 ([Wikipedia: Inode pointer structure](https://en.wikipedia.org/wiki/Inode_pointer_structure)). The *real* limit of a particular file system also depends on other fields, such as the width of the size field in the inode, so these figures illustrate the scheme and are not the specification of any one system.

## 🔗 Linked Allocation in Practice: the FAT

Pure linked allocation, with the pointer inside each data block, is painfully slow and fragile: one damaged block loses the rest of the file. The **File Allocation Table** (FAT) file system keeps the same idea but moves the pointers out of the data blocks and into a table at the start of the volume, with one entry per cluster. Each entry holds the number of the next cluster of the file, or a marker for the end of the file, for unused space, or for reserved areas; the directory entry holds the number of the file's first cluster, and the operating system follows the chain through the table until it reaches the end ([Wikipedia: File Allocation Table](https://en.wikipedia.org/wiki/File_Allocation_Table)). The table is small enough to be cached in memory, so following a chain costs memory accesses, not disk reads. FAT was developed in 1977 for floppy disks and was the default file system of DOS and Windows 9x (the same article). The table of the scenario above, for the linked allocator, looks like this:

```python
END = "end"

def fat_table(disk):
    """The File Allocation Table of a disk managed by linked allocation: for each block, the next block of its file."""
    table = {}
    for blocks in disk.files.values():
        for here, following in zip(blocks, blocks[1:] + [END]):
            table[here] = following
    return table

disk = LinkedDisk(24)
for name, count in (("A", 6), ("B", 4), ("C", 6), ("D", 4), ("F", 4)):
    disk.create(name, count)
disk.delete("B")
disk.delete("D")
disk.create("E", 6)
table = fat_table(disk)
first_block_of_E = disk.files["E"][0]                           # the only thing the directory entry needs to store
chain, here = [], first_block_of_E
while here != END:
    chain.append(here)
    here = table[here]
print("the directory entry of E holds block", first_block_of_E, "| following the table:", " -> ".join(map(str, chain)), "-> end")
print("table entries for E:", {block: table[block] for block in disk.files["E"]})
```

```text
the directory entry of E holds block 6 | following the table: 6 -> 7 -> 8 -> 9 -> 16 -> 17 -> end
table entries for E: {6: 7, 7: 8, 8: 9, 9: 16, 16: 17, 17: 'end'}
```

E's chain jumps from block 9 to block 16, which is exactly the scattering that made the allocation possible. A FAT volume pays for it by keeping the whole table consistent (usually in two copies), and a file that is badly scattered reads slowly on a spinning disk, because the head must move between the pieces.

## 📐 Extents: Ranges Instead of Pointers

Instead of listing every block of a file, a file system can list **extents**: contiguous runs of blocks, each stored compactly as a pair (start, length) instead of one number per block. A file consists of zero or more extents, and one fragment of a file needs one extent. Extents allow the compact description of large files and reduce fragmentation, because the file system tries to allocate in runs ([Wikipedia: Extent (file systems)](https://en.wikipedia.org/wiki/Extent_(file_systems))). They are used by APFS, the file system of the Mac used here, as well as by Btrfs and by ext4, in which they have been the default since Linux 2.6.23 (the same article). The function `extents` of the code above converts a list of blocks into runs. Compare the bookkeeping for a 1 GiB file with 4 KiB blocks:

```python
blocks_in_a_gibibyte = 2**30 // 4096
one_run = list(range(1000, 1000 + blocks_in_a_gibibyte))
two_pieces = one_run[:100_000] + [b + 50_000 for b in one_run[100_000:]]
print(f"as one block pointer per block: {len(one_run):,} pointers")
print("as extents, allocated in one run:", extents(one_run))
print("as extents, if the file was split in two pieces:", len(extents(two_pieces)), "extents")
print("extents of file E in the scenario above:", extents(disk.files["E"]))
```

```text
as one block pointer per block: 262,144 pointers
as extents, allocated in one run: [(1000, 262144)]
as extents, if the file was split in two pieces: 2 extents
extents of file E in the scenario above: [(6, 4), (16, 2)]
```

A file stored in one run needs one entry instead of 262,144, and even a file in a few pieces needs only a few. Extents keep the benefit of contiguous allocation (compact, fast sequential access) and avoid its problem, because a file that cannot get one run can use several.

## 🧪 An Experiment: a Nearly Full Disk

Which policy copes best when a disk is 85% full and files keep coming and going? The experiment runs a stream of random file creations (1 to 60 blocks each) and deletions on a 2,000-block disk, keeping it about 85% full, with three policies: *contiguous* (first run that fits), *scatter* (the lowest-numbered free blocks, wherever they are, as in the linked and indexed methods above), and *extent-aware* (use the snuggest single run that fits, and only if there is none, fill the biggest free runs first). It reports the share of creations that were refused and the average number of extents per file, which measures fragmentation:

```python
import random

def free_runs(disk):
    """The runs of free blocks, as (start, length)."""
    runs, start = [], None
    for block in range(disk.size + 1):
        is_free = block < disk.size and disk.owner[block] is None
        if is_free and start is None:
            start = block
        elif not is_free and start is not None:
            runs.append((start, block - start))
            start = None
    return runs

class ExtentDisk(Disk):
    """Extent-aware allocation: use the snuggest single run if one fits; otherwise take the biggest runs first."""

    def create(self, name, count):
        runs = free_runs(self)
        if sum(length for _, length in runs) < count:
            return None
        fitting = [run for run in runs if run[1] >= count]
        if fitting:
            start, _ = min(fitting, key=lambda run: run[1])
            return self._give(name, range(start, start + count))
        chosen, needed = [], count
        for start, length in sorted(runs, key=lambda run: -run[1]):
            take = min(length, needed)
            chosen.extend(range(start, start + take))
            needed -= take
            if needed == 0:
                break
        return self._give(name, sorted(chosen))

def churn(kind, seed, size=2000, target=0.85, creates=1000):
    rng = random.Random(seed)
    disk, live, refused = kind(size), [], 0
    for serial in range(creates):
        while live and size - len(disk.free_blocks()) > target * size:        # too full: some file is deleted
            disk.delete(live.pop(rng.randrange(len(live))))
        name = f"f{serial}"
        if disk.create(name, rng.randint(1, 60)) is None:
            refused += 1
        else:
            live.append(name)
    pieces = sum(len(extents(disk.files[name])) for name in live)
    return refused, creates, pieces, len(live)

print(f"{'policy':<30} {'creations refused':>17} {'extents per file':>16}")
for label, kind in (("contiguous (first fit)", ContiguousDisk), ("scatter (lowest free blocks)", LinkedDisk), ("extent-aware", ExtentDisk)):
    refused = creates = pieces = files = 0
    for seed in range(6):
        r, c, p, f = churn(kind, seed)
        refused, creates, pieces, files = refused + r, creates + c, pieces + p, files + f
    print(f"{label:<30} {refused / creates:>17.1%} {pieces / files:>16.2f}")
```

```text
policy                         creations refused extents per file
contiguous (first fit)                     28.3%             1.00
scatter (lowest free blocks)                0.0%             9.34
extent-aware                                0.0%             1.11
```

Contiguous allocation refuses about three creations in ten although the disk is never more than 85% full, simply because no single run is long enough. Scattering never refuses, but it shreds files into more than nine pieces each on average, which costs head movement on a spinning disk and bookkeeping everywhere. The extent-aware policy gets the best of both: nothing refused and about 1.1 extents per file. This is the policy idea behind the allocators of ext4, APFS, and NTFS, and it is why those systems cope well with long-lived, heavily used disks. (Solid-state drives have no moving head, so for them fragmentation costs mostly metadata and the number of operations rather than seek time.)

## 📋 The Methods Compared

| | Contiguous | Linked (FAT) | Indexed (inode) | Extents |
|--|------------|--------------|-----------------|---------|
| **External fragmentation** | Yes: files need one run | No | No | Little: runs are used when they exist |
| **Random access** | One read | Follow the chain (a cached table makes it cheap) | One to four reads | Search a short list of ranges |
| **Growth** | Hard: may need to move the file | Easy | Easy | Easy: add an extent |
| **Bookkeeping per file** | Two numbers | One entry per block, in the table | A few pointers, plus indirect blocks for big files | One pair per fragment |
| **Used by** | Early systems, CD-ROMs | FAT, in DOS, Windows 9x, and today's removable media | UFS, ext2, ext3 | ext4, NTFS, APFS, Btrfs |

## ✅ Checking the Code

The allocators were tested against independent checks on random operations. On random sequences of creations and deletions, every method kept the bookkeeping consistent: no block was ever owned by two files, owned and free blocks always added up to the disk size, and a file's blocks were exactly the ones it had been given. `reads_to_reach` was compared with the cost of walking an explicitly built tree of indirect blocks (for small parameters that exercise all the levels), and the maximum file size with the number of block addresses that tree holds. `extents` was checked by expanding its runs back into the original blocks. And the extent-aware allocator always returned exactly the requested number of free blocks, in a single run whenever a free run that long existed.

## Common Misconceptions

- **"Contiguous allocation is the best, since it is the fastest."** It is the fastest to read, but it suffers from external fragmentation: in the experiment, a disk that was at most 85% full refused about three creations in ten.
- **"The FAT is a table of files."** It is a table of *clusters*, with one entry per cluster telling where the file continues; the directory holds each file's first cluster.
- **"A file that needs an indirect block is slow to read."** One extra read, and only for the part of the file beyond the direct blocks; caching usually hides it, and most files are small enough to need none.
- **"Extents replaced block pointers because they are faster."** They are more compact for the typical file and they reduce fragmentation, though for the *overall* storage efficiency the savings are slight compared with the amount of data stored, as Wikipedia notes ([Wikipedia: Extent (file systems)](https://en.wikipedia.org/wiki/Extent_(file_systems))).
- **"Fragmentation only matters on spinning disks."** It matters less on SSDs, but it still costs metadata space and extra operations.

## ➡️ Next

Continue to [file-permissions.md](file-permissions.md): who may do what to a file, how permission bits and directory permissions work, and what the special bits and access control lists add. The lesson after it, [file-system-security.md](file-system-security.md), covers the classic ways in which file systems are attacked and defended.
