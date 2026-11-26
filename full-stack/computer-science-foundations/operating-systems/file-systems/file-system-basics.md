# 🗄️ File System Basics

## From Numbered Blocks to Named Files

A disk, whether spinning or solid-state, offers nothing but a long row of numbered blocks that can be read and written. No program wants to think in blocks. Programs want *named, durable, protected collections of bytes* that survive a reboot and can be found again by name. The **file system** is the part of the operating system that provides them. It governs how files are organized and accessed, and it lets many applications share mass storage; without one, applications could reach the storage in incompatible ways, with resource contention, corrupted data, and lost data as the result ([Wikipedia: File system](https://en.wikipedia.org/wiki/File_system)). A file system has five jobs:

| Job | What it means |
|-----|---------------|
| **Naming and organization** | Give files names, group them in directories, and find a file from its name |
| **Space management** | Decide which blocks belong to which file, and keep track of the free ones |
| **Metadata** | Remember each file's size, owner, permissions, and times, apart from its contents |
| **Protection and sharing** | Decide who may read, write, or run what, and let permitted users share files safely |
| **Reliability** | Keep the structures consistent, even when the machine stops in the middle of an update |

This file looks at the whole picture: the layers between a program and the disk, what a volume contains, how a file system on your own machine allocates space (with measurements), and why updates must be done carefully. The following files go deeper into [files and directories](files-and-directories.md), [how blocks are allocated to files](file-allocation.md), [who may access them](file-permissions.md), and [how they are attacked and defended](file-system-security.md). All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); file systems differ, so each machine-dependent result is labelled, and the code runs unchanged on Linux.

## 🧅 The Layers Between a Program and the Disk

A local file system can be described as layers of abstraction, even though a particular design may not separate them so cleanly ([Wikipedia: File system](https://en.wikipedia.org/wiki/File_system)):

```
 your program         open("notes.txt"), read, write, close
      │
 system calls         open(2), read(2), write(2), stat(2), ...        the interface of the kernel
      │
 logical file system  names, directories, permissions, open-file table, file descriptors
      │
 virtual file system  one interface in front of many different file system types
      │
 physical file system the real layout on disk (APFS, ext4, NTFS, FAT, ...): which blocks hold what
      │
 block layer / driver reads and writes numbered blocks on the device
      │
 the device           SSD, hard disk, USB stick, network volume
```

The **logical file system** offers the programming interface for operations such as open, close, read, and write, manages the table of open files and the per-process file descriptors of [what-is-a-process.md](../processes-and-threads/what-is-a-process.md), and enforces security and protection. The **physical file system** at the bottom reads and writes data blocks, buffers them, and controls where on the medium they are placed (the same article). Between them, the **virtual file system** (VFS) lets several different file system types exist side by side: in Linux it is the software layer in the kernel that provides the filesystem interface to user programs and lets different filesystem implementations coexist ([Linux kernel documentation: Overview of the Linux VFS](https://docs.kernel.org/filesystems/vfs.html)). That is why the same `open` call works on your internal drive, a USB stick with a different format, and a network share: the program sees one interface, and the VFS routes each call to the right implementation. Every program in this module has used that interface, from Python's `open` down to the system calls of [what-is-an-operating-system.md](../introduction-to-operating-systems/what-is-an-operating-system.md).

## 🧱 What Is on a Volume

A **volume** (a formatted disk or partition) holds a few kinds of structure, with different names in different file systems:

- **A superblock or volume header**, near the start, that says what kind of file system this is, how big its blocks are, and where everything else is.
- **A map of free space**, a bitmap or a list of free extents, so that the system can find blocks for new data ([file-allocation.md](file-allocation.md)).
- **Metadata records**, one per file: Unix-style systems call them **inodes**, NTFS has its master file table, and so on. A file system stores a file's metadata (name, size, creation, access and modification times, owner and group, permissions, and attributes) separately from the file's content ([Wikipedia: File system](https://en.wikipedia.org/wiki/File_system)).
- **Directories**, which map names to files, and are usually stored like any other file (the same article).
- **Data blocks**, which hold the contents of files.
- Often a **journal**, a log used to keep the structures consistent after a crash (below).

## 🔎 Looking at Your Own Volume

Python can ask the operating system about the volume that holds a folder. `os.statvfs` reports two block sizes that are easy to confuse: `f_frsize`, the fundamental unit in which space is allocated, and `f_bsize`, the preferred size for transfers; the file system type comes from the `mount` command:

```python
import os
import re
import shutil
import subprocess
import tempfile

folder = tempfile.gettempdir()
info = os.statvfs(folder)
print(f"allocation unit (f_frsize): {info.f_frsize:,} bytes | preferred transfer size (f_bsize): {info.f_bsize:,} bytes")
total, used, free = shutil.disk_usage(folder)
print(f"the volume holding the temporary files: {total / 2**30:,.0f} GiB in total, {used / 2**30:,.0f} GiB used ({used / total:.0%}), {free / 2**30:,.0f} GiB free")
print(f"file records (inodes) in total: {info.f_files:,}, free: {info.f_ffree:,}")

device = subprocess.run(["df", "-P", folder], capture_output=True, text=True).stdout.splitlines()[-1].split()[0]
for line in subprocess.run(["mount"], capture_output=True, text=True).stdout.splitlines():
    if line.startswith(device + " "):
        kind = re.search(r"\((\w+)[,)]", line) or re.search(r" type (\w+) ", line)
        print("device:", device, "| file system type:", kind.group(1) if kind else "unknown")
        break
```

One run on the test machine printed:

```
allocation unit (f_frsize): 4,096 bytes | preferred transfer size (f_bsize): 1,048,576 bytes
the volume holding the temporary files: 460 GiB in total, 207 GiB used (45%), 254 GiB free
file records (inodes) in total: 2,661,108,490, free: 2,659,086,960
device: /dev/disk3s5 | file system type: apfs
```

The figures describe the Mac used for this module, whose file system is APFS. Two things are worth noticing. Space is handed out in units of 4,096 bytes, though the system prefers to move data in much larger chunks, a megabyte here. And the number of file records is huge and, on this file system, not fixed in advance; in older designs such as ext4 the number of inodes is fixed when the volume is created, so a disk can be "full" of tiny files while having gigabytes of free space.

## 📦 Space Is Handed Out in Whole Blocks

Because a file system allocates in whole blocks, a file's allocated size is rounded up to a multiple of the allocation unit, and the unused tail of the last block, **slack space**, is wasted: the internal fragmentation of [memory-allocation.md](../memory-management/memory-allocation.md), on disk. The classic illustration is a folder of tiny files. With 4,096-byte clusters, 100,000 files of five bytes each hold 500,000 bytes of data but occupy 409,600,000 bytes of disk ([Wikipedia: File system](https://en.wikipedia.org/wiki/File_system)), which the first block of code below reproduces by arithmetic. The second block measures the real thing: it writes files of different sizes and asks the system, with `os.stat`, both for the size in bytes and for the space actually allocated (`st_blocks` counts 512-byte units):

```python
files, size, cluster = 100_000, 5, 4096
print(f"{files:,} files of {size} bytes hold {files * size:,} bytes of data but occupy {files * cluster:,} bytes ({cluster / size:,.0f} times as much)")
```

```text
100,000 files of 5 bytes hold 500,000 bytes of data but occupy 409,600,000 bytes (819 times as much)
```

```python
with tempfile.TemporaryDirectory() as workshop:
    print(f"{'size in bytes':>14} | {'allocated':>10} | {'wasted':>8}")
    for size in (0, 1, 100, 4096, 4097, 10_000, 100_000):
        path = os.path.join(workshop, f"file{size}")
        with open(path, "wb") as handle:
            handle.write(b"x" * size)
        status = os.stat(path)
        allocated = status.st_blocks * 512
        print(f"{status.st_size:>14,} | {allocated:>10,} | {allocated - status.st_size:>8,}")
```

One run on the test machine printed:

```
 size in bytes |  allocated |   wasted
             0 |          0 |        0
             1 |      4,096 |    4,095
           100 |      4,096 |    3,996
         4,096 |      4,096 |        0
         4,097 |      8,192 |    4,095
        10,000 |     12,288 |    2,288
       100,000 |    102,400 |    2,400
```

The empty file occupies no data block at all, a one-byte file takes a whole 4,096-byte block, a file one byte over a block boundary takes two, and on average a file wastes about half a block. The Python documentation notes that `st_blocks` can also be smaller than the file size divided by 512 when the file has holes, which is the next experiment ([Python docs: `os`](https://docs.python.org/3/library/os.html)).

## 🕳️ Sparse Files: the Size of a File Is Not the Space It Uses

A file is not a literal row of bytes on disk; it is a *mapping* from byte offsets to blocks, and some offsets may have no block behind them. If a program seeks far past the end of a file and writes there, many file systems do not allocate the skipped range at all: reading it returns zeros. Such a **sparse file** looks huge but uses little space:

```python
with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "sparse")
    with open(path, "wb") as handle:
        handle.seek(100 * 1024 * 1024)               # skip 100 MiB without writing anything
        handle.write(b"end")
    status = os.stat(path)
    print(f"size reported: {status.st_size:,} bytes | space allocated: {status.st_blocks * 512:,} bytes")
    with open(path, "rb") as handle:
        handle.seek(50 * 1024 * 1024)
        print("a byte from the middle of the hole reads as:", handle.read(1))
```

One run on the test machine printed:

```
size reported: 104,857,603 bytes | space allocated: 4,096 bytes
a byte from the middle of the hole reads as: b'\x00'
```

The file claims to be about 100 MiB, but only the block holding the three bytes at the end exists. (Whether holes are supported depends on the file system; on one that does not, the whole range would be allocated and filled with zeros.) This is the same idea as virtual memory in [paging.md](../memory-management/paging.md): a *logical* range of addresses, of which only the parts that are used are backed by real blocks.

## 💥 Surviving a Crash: Why Updates Must Be Careful

Writing a file changes several structures: the data blocks, the file's metadata record, the free-space map, and the directory entry that names it. Bringing a file system up to date usually takes many separate writes, so a power failure or crash between them can leave the structures in an invalid intermediate state. Deleting a file on a Unix file system, for example, takes three steps (remove the directory entry, release the inode to the pool of free inodes, and return the data blocks to the pool of free blocks), and a crash between the first two leaves an inode that nothing names ([Wikipedia: Journaling file system](https://en.wikipedia.org/wiki/Journaling_file_system)). File systems answer this in three main ways. Older ones repair the damage after a crash by checking the whole volume, which takes longer as disks grow ([OSTEP: Crash Consistency, FSCK and Journaling](https://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf)). A **journaling** file system first records the goal of each change in a journal, usually a circular log, so that after a crash it can be brought back online quickly and with a lower likelihood of corruption (the same Wikipedia article); some journal only metadata, which is faster but leaves data less protected, and others journal data as well. And some designs never overwrite live records: Apple's APFS, the file system of the Mac used here, writes entirely new metadata records, points to them, and only then releases the old ones (**redirect-on-write**), so that a crash cannot leave a record that is part old and part new ([Wikipedia: Apple File System](https://en.wikipedia.org/wiki/Apple_File_System)).

Applications have a similar problem. If a program overwrites a configuration file in place and the machine stops half-way, the file is left half-old and half-new. The standard remedy uses an operation the file system guarantees to be atomic: write the new version to a temporary file in the same directory, force it to disk, and **rename** it over the old name. When the new name already exists, rename replaces it atomically, so that no process ever finds it missing ([Linux man page: `rename(2)`](https://man7.org/linux/man-pages/man2/rename.2.html)); in Python `os.replace` does this on every platform, and `os.fsync` forces a file's data to the device (the same rule applies: flush the Python buffer first):

```python
def replace_atomically(path, data):
    """Replace the contents of `path` so that a reader sees either the old version or the new one, never a mixture."""
    folder = os.path.dirname(path)
    descriptor, temporary = tempfile.mkstemp(dir=folder)         # a new file in the same directory (same volume)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())                                # the new contents are on the device before the rename
    os.replace(temporary, path)                                  # one atomic step: the name now refers to the new file

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "settings.conf")
    replace_atomically(path, b"mode = fast\n")
    old_inode = os.stat(path).st_ino
    replace_atomically(path, b"mode = safe\n")
    print("contents now:", open(path, "rb").read())
    print("the name now refers to a different file record:", os.stat(path).st_ino != old_inode)
    print("files left in the folder:", os.listdir(workshop))
```

```text
contents now: b'mode = safe\n'
the name now refers to a different file record: True
files left in the folder: ['settings.conf']
```

The name `settings.conf` was never without a complete file: before the rename it meant the old file, and afterwards the new one. No temporary file is left over. Producing the half-written case on purpose would mean crashing the machine, so this lesson describes it rather than demonstrating it.

## Common Misconceptions

- **"A file is a contiguous run of bytes on the disk."** It is a mapping from offsets to blocks that may be scattered (and, for sparse files, missing).
- **"A file's size is the space it uses."** Space is allocated in whole blocks, so a one-byte file takes a block, and a sparse file can claim far more than it occupies.
- **"The free space on the disk is the only limit."** There can also be a limit on the number of file records, and on a volume full of tiny files it can be reached first.
- **"A file system is the same as a disk format."** It also includes the code that interprets the format and the interface that programs use; the VFS lets one kernel serve many formats.
- **"Saving a file is a single step."** It touches several structures, which is why file systems need journals or copy-on-write, and why applications should write to a temporary file and rename it.

## ➡️ Next

Continue to [files-and-directories.md](files-and-directories.md): how a name leads to a file (inodes, directories, and path resolution), what hard links and symbolic links really are, and what a file descriptor refers to.
