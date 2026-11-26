# 📁 Files and Directories

## A File Is Not Its Name

On the screen, a file is its name: `notes.txt`. Inside a Unix-style file system, a name is only a *label* that points at the real object. The object is described by a record called an **inode** (index node), a data structure that stores the file's attributes, such as owner, permissions, and times, and the locations of its data blocks ([Wikipedia: Inode](https://en.wikipedia.org/wiki/Inode)). Each inode is identified by a number, and the name is stored somewhere else: in a **directory**, which is simply a list of names with the inode numbers they refer to (the same article). Keeping the name out of the file explains behaviour that otherwise looks odd: a file can have several names, can be renamed without touching its data, and can keep existing after its name has been removed.

This file follows that idea through the whole interface: what the system remembers about a file, how names lead to files, the difference between hard links and symbolic links, what a file descriptor points to, and how a path is resolved, ending with a small working model of all of it. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon); the experiments run on Linux unchanged, and file systems differ in details, so the machine-dependent results are labelled.

## 🧾 What the System Knows About a File

Each file has an inode that holds metadata about the file, which a program can retrieve with the `stat` system call ([Linux man page: `inode(7)`](https://man7.org/linux/man-pages/man7/inode.7.html)). The usual fields, with the names Python's `os.stat` gives them, are:

| Metadata | `os.stat` field | Meaning |
|----------|-----------------|---------|
| File type and permissions | `st_mode` | Regular file, directory, symbolic link, and so on, plus the read, write, and execute bits |
| Inode number | `st_ino` | The file's identity within its volume |
| Link count | `st_nlink` | The number of hard links, that is, names, that refer to the inode |
| Owner and group | `st_uid`, `st_gid` | Who owns the file |
| Size | `st_size` | Length in bytes |
| Allocation | `st_blocks`, `st_blksize` | Space actually allocated, and the preferred I/O size |
| Times | `st_atime`, `st_mtime`, `st_ctime` | Last access, last content change, last metadata change |

The file's *name* is not in the table, because it is not part of the file. The next block creates a file and reads back some of its metadata:

```python
import errno
import os
import stat
import tempfile

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "file")
    with open(path, "w") as handle:
        handle.write("hello")
    status = os.stat(path)
    print("a regular file:", stat.S_ISREG(status.st_mode), "| size in bytes:", status.st_size, "| names (links):", status.st_nlink)
    print("owned by this user:", status.st_uid == os.getuid(), "| the inode number is an integer:", isinstance(status.st_ino, int))
    print("the three timestamps are seconds since 1970:", all(isinstance(moment, float) for moment in (status.st_atime, status.st_mtime, status.st_ctime)))
```

```text
a regular file: True | size in bytes: 5 | names (links): 1
owned by this user: True | the inode number is an integer: True
the three timestamps are seconds since 1970: True
```

## 🔗 Many Names, One File: Hard Links and Symbolic Links

A **hard link** is just a directory entry that associates a name with a file, which means that every file has at least one. Creating another hard link makes the same contents reachable through another path: a process can open the file by any of its names and change the content, and no name is the "original" ([Wikipedia: Hard link](https://en.wikipedia.org/wiki/Hard_link); [Linux man page: `link(2)`](https://man7.org/linux/man-pages/man2/link.2.html)). A **symbolic link** is different: it is an independent file whose contents are a path. The path is followed whenever the link is used, so the link refers to a *name*, not to an object. Deleting the link does not affect its target, and if the target is deleted or renamed the link is not updated, and it dangles ([Wikipedia: Symbolic link](https://en.wikipedia.org/wiki/Symbolic_link); [Linux man page: `symlink(7)`](https://man7.org/linux/man-pages/man7/symlink.7.html)). The experiment below makes one of each and then removes the original name:

```python
with tempfile.TemporaryDirectory() as workshop:
    original = os.path.join(workshop, "original.txt")
    with open(original, "w") as handle:
        handle.write("hello")
    hard = os.path.join(workshop, "hard.txt")
    soft = os.path.join(workshop, "soft.txt")
    os.link(original, hard)                                         # a second name for the same inode
    os.symlink(original, soft)                                      # a new file that contains the path of the first
    a, b, c = os.stat(original), os.stat(hard), os.lstat(soft)      # lstat looks at the link itself, not its target
    print("hard link shares the inode:", a.st_ino == b.st_ino, "| link count of the file:", a.st_nlink)
    print("symbolic link has an inode of its own:", c.st_ino != a.st_ino, "| its size is the length of the path it holds:", c.st_size == len(original))
    os.remove(original)                                             # remove one name
    print("after removing the original name, the data is still there:", repr(open(hard).read()), "| link count now", os.stat(hard).st_nlink)
    print("the symbolic link still exists:", os.path.lexists(soft), "| but it dangles (its target is gone):", not os.path.exists(soft))
```

```text
hard link shares the inode: True | link count of the file: 2
symbolic link has an inode of its own: True | its size is the length of the path it holds: True
after removing the original name, the data is still there: 'hello' | link count now 1
the symbolic link still exists: True | but it dangles (its target is gone): True
```

Removing a file with `os.remove` (the `unlink` system call) deletes a *name*. If it was the last name and no process has the file open, the file is deleted and its space can be reused; if processes still have it open, the file remains in existence until the last descriptor referring to it is closed ([Linux man page: `unlink(2)`](https://man7.org/linux/man-pages/man2/unlink.2.html)). Many file systems refuse hard links to directories, because directories are themselves files that contain names, and several links to them could create a circular structure instead of a tree ([Wikipedia: Hard link](https://en.wikipedia.org/wiki/Hard_link)); the Mac used for this module is one of them, as an experiment below shows. A hard link cannot refer to a file on a different volume either, since inode numbers are meaningful only inside one volume; a symbolic link has neither restriction ([Linux man page: `symlink(7)`](https://man7.org/linux/man-pages/man7/symlink.7.html)).

## 🔢 What a File Descriptor Points To

When a program opens a file, the kernel does not hand out the inode. Opening creates a new **open file description**, an entry in the system-wide table of open files that records the current *offset* and the status flags, and the **file descriptor** that the program receives is a reference to that entry ([Linux man page: `open(2)`](https://man7.org/linux/man-pages/man2/open.2.html)). Three tables are therefore involved, which the Wikipedia article on inodes draws as a figure: each process has its own table of descriptors; these point into the system-wide table of open file descriptions; and these point to the inodes. Two descriptors can refer to the *same* description (made by `dup`, or inherited across `fork`), and then they share one offset; two separate `open` calls create two descriptions, with independent offsets. The experiment reads from a file holding the digits 0 to 9:

```python
with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "digits")
    with open(path, "wb") as handle:
        handle.write(b"0123456789")
    first = os.open(path, os.O_RDONLY)
    second = os.open(path, os.O_RDONLY)                             # a separate open: a new open file description
    shared = os.dup(first)                                          # a copy of the descriptor: the same open file description
    print("first reads", os.read(first, 3), "| second (opened again) reads", os.read(second, 3), "| the dup of first reads", os.read(shared, 3))
    child = os.fork()                                               # the child inherits the descriptor and shares the description
    if child == 0:
        os._exit(0 if os.read(first, 2) == b"67" else 1)
    _, status = os.waitpid(child, 0)
    print("the child read b'67' through the shared description:", os.waitstatus_to_exitcode(status) == 0, "| the parent now reads", os.read(first, 2))
    for descriptor in (first, second, shared):
        os.close(descriptor)

    held = os.open(path, os.O_RDONLY)
    os.unlink(path)                                                 # remove the only name while the file is open
    print("the name is gone:", not os.path.exists(path), "| link count seen through the descriptor:", os.fstat(held).st_nlink, "| the data is still readable:", os.read(held, 4))
    os.close(held)
```

```text
first reads b'012' | second (opened again) reads b'012' | the dup of first reads b'345'
the child read b'67' through the shared description: True | the parent now reads b'89'
the name is gone: True | link count seen through the descriptor: 0 | the data is still readable: b'0123'
```

The separate `open` started again from the beginning (`012`), while the duplicate continued where `first` had stopped (`345`); and the child's read advanced the offset that the parent then continued from (`89`), because parent and child share the open file description. The last experiment shows that a name and a file are separate things: with the only name removed, the link count is 0, yet the data stays readable through the descriptor and disappears only when the descriptor is closed. A well-known use is a program that creates a temporary file and unlinks it at once, so that nothing is left behind if the program crashes.

## 🌳 Directories and Path Resolution

A directory is a list of names with the inodes they refer to; Wikipedia's article on inodes adds that on Unix-style systems it contains an entry for itself (`.`), its parent (`..`), and each child. Directories that can contain directories give a hierarchy, and the first file system to support arbitrary hierarchies was used in Multics; today's file systems all support them ([Wikipedia: File system](https://en.wikipedia.org/wiki/File_system)). To turn a path into a file, the kernel does **path resolution**. Starting from the root (or from the process's current directory for a relative path), it looks up each component in the current directory: if the process lacks search permission on that directory, the lookup fails with a permission error; if the component does not exist, with "no such file or directory"; if it exists but is neither a directory nor a link when more components follow, with "not a directory". A symbolic link met on the way is resolved first, and to guard against links that lead back to themselves, there is a limit on the number of links followed, which is 40 on Linux, after which the error is "too many levels of symbolic links" ([Linux man page: `path_resolution(7)`](https://man7.org/linux/man-pages/man7/path_resolution.7.html)).

The class below models all of this in about 140 lines: an in-memory file system with numbered inodes, directories that map names to inode numbers, hard links with link counts, symbolic links, and path resolution with the link limit (set to 8 here to keep examples short). Because an inode is freed when its link count reaches zero, deleting a name behaves just as in the experiments above:

```python
import errno

class MiniFS:
    """A tiny in-memory file system: numbered inodes, directories that map names to inode numbers, hard links, and symbolic links."""

    MAX_SYMLINKS = 8

    def __init__(self):
        self.inodes = {}                            # inode number -> {"kind": "file" | "dir" | "symlink", "links": count, ...}
        self.next_number = 1
        self.root = self._new("dir")
        self.inodes[self.root]["entries"] = {}

    def _new(self, kind, **fields):
        number, self.next_number = self.next_number, self.next_number + 1
        self.inodes[number] = {"kind": kind, "links": 0, **fields}
        return number

    def _split(self, path):
        return [part for part in path.split("/") if part]

    def _walk(self, path, follow_last=True, depth=0):
        """Return (directory inode, name, inode or None) for `path`, following symbolic links on the way."""
        if depth > self.MAX_SYMLINKS:
            raise OSError(errno.ELOOP, "too many levels of symbolic links")
        parts = self._split(path)
        directory, name, current = self.root, "", self.root
        for position, part in enumerate(parts):
            node = self.inodes[current]
            if node["kind"] != "dir":
                raise NotADirectoryError(path)
            directory, name = current, part
            current = node["entries"].get(part)
            last = position == len(parts) - 1
            if current is None:
                if last:
                    return directory, name, None
                raise FileNotFoundError(path)
            if self.inodes[current]["kind"] == "symlink" and (follow_last or not last):
                rest = "/".join(parts[position + 1:])
                target = self.inodes[current]["target"]
                base = "/".join(parts[:position])
                resolved = target if target.startswith("/") else base + "/" + target
                return self._walk(resolved + ("/" + rest if rest else ""), follow_last, depth + 1)
        if not parts:
            return None, "", self.root
        return directory, name, current

    def mkdir(self, path):
        directory, name, inode = self._walk(path, follow_last=False)
        if inode is not None:
            raise FileExistsError(path)
        self.inodes[directory]["entries"][name] = self._new("dir", entries={}, links=1)

    def write(self, path, data):
        directory, name, inode = self._walk(path)                     # like open(path, "w"): follows a final symbolic link
        if inode is None:
            inode = self._new("file", data="")
            self.inodes[directory]["entries"][name] = inode
            self.inodes[inode]["links"] = 1
        elif self.inodes[inode]["kind"] == "dir":
            raise IsADirectoryError(path)
        self.inodes[inode]["data"] = data

    def read(self, path):
        directory, name, inode = self._walk(path)
        if inode is None:
            raise FileNotFoundError(path)
        if self.inodes[inode]["kind"] == "dir":
            raise IsADirectoryError(path)
        return self.inodes[inode]["data"]

    def link(self, existing, new):
        _, _, inode = self._walk(existing, follow_last=False)
        if inode is None:
            raise FileNotFoundError(existing)
        if self.inodes[inode]["kind"] == "dir":
            raise PermissionError("hard links to directories are not allowed")
        directory, name, taken = self._walk(new, follow_last=False)
        if taken is not None:
            raise FileExistsError(new)
        self.inodes[directory]["entries"][name] = inode
        self.inodes[inode]["links"] += 1

    def symlink(self, target, path):
        directory, name, taken = self._walk(path, follow_last=False)
        if taken is not None:
            raise FileExistsError(path)
        inode = self._new("symlink", target=target)
        self.inodes[inode]["links"] = 1
        self.inodes[directory]["entries"][name] = inode

    def unlink(self, path):
        directory, name, inode = self._walk(path, follow_last=False)
        if inode is None:
            raise FileNotFoundError(path)
        if self.inodes[inode]["kind"] == "dir":
            raise IsADirectoryError(path)
        del self.inodes[directory]["entries"][name]
        self.inodes[inode]["links"] -= 1
        if self.inodes[inode]["links"] == 0:                           # nothing names the inode any more: free it
            del self.inodes[inode]

    def rmdir(self, path):
        directory, name, inode = self._walk(path, follow_last=False)
        if inode is None:
            raise FileNotFoundError(path)
        if self.inodes[inode]["kind"] != "dir":
            raise NotADirectoryError(path)
        if self.inodes[inode]["entries"]:
            raise OSError(errno.ENOTEMPTY, "directory not empty")
        del self.inodes[directory]["entries"][name]
        del self.inodes[inode]

    def listdir(self, path):
        _, _, inode = self._walk(path)
        if inode is None:
            raise FileNotFoundError(path)
        if self.inodes[inode]["kind"] != "dir":
            raise NotADirectoryError(path)
        return sorted(self.inodes[inode]["entries"])

    def links(self, path):
        _, _, inode = self._walk(path, follow_last=False)
        if inode is None:
            raise FileNotFoundError(path)
        return self.inodes[inode]["links"]

    def inode_of(self, path):
        _, _, inode = self._walk(path, follow_last=False)
        return inode

    def readlink(self, path):
        _, _, inode = self._walk(path, follow_last=False)
        if inode is None:
            raise FileNotFoundError(path)
        if self.inodes[inode]["kind"] != "symlink":
            raise OSError(errno.EINVAL, "not a symbolic link")
        return self.inodes[inode]["target"]
```

The next block builds a small tree and replays the experiments of this file on the model:

```python
fs = MiniFS()
fs.mkdir("/home")
fs.mkdir("/home/ana")
fs.write("/home/ana/notes.txt", "remember the milk")
fs.link("/home/ana/notes.txt", "/home/ana/copy.txt")                # a second name for the same inode
fs.symlink("/home/ana/notes.txt", "/home/ana/shortcut")             # a file that holds a path

print("names in /home/ana:", fs.listdir("/home/ana"))
print("link count of notes.txt:", fs.links("/home/ana/notes.txt"), "| same inode as copy.txt:", fs.inode_of("/home/ana/notes.txt") == fs.inode_of("/home/ana/copy.txt"))
print("reading through the symbolic link:", fs.read("/home/ana/shortcut"))

fs.unlink("/home/ana/notes.txt")                                    # remove one name
print("after unlinking notes.txt:", fs.listdir("/home/ana"), "| link count of copy.txt:", fs.links("/home/ana/copy.txt"), "| copy.txt still reads:", fs.read("/home/ana/copy.txt"))
try:
    fs.read("/home/ana/shortcut")
except FileNotFoundError:
    print("the shortcut now dangles: its target name no longer exists")

fs.symlink("/loop2", "/loop1")
fs.symlink("/loop1", "/loop2")
try:
    fs.read("/loop1")
except OSError as error:
    print("two links pointing at each other:", errno.errorcode[error.errno])

try:
    fs.link("/home", "/home/again")
except PermissionError:
    print("a hard link to a directory is refused")
```

```text
names in /home/ana: ['copy.txt', 'notes.txt', 'shortcut']
link count of notes.txt: 2 | same inode as copy.txt: True
reading through the symbolic link: remember the milk
after unlinking notes.txt: ['copy.txt', 'shortcut'] | link count of copy.txt: 1 | copy.txt still reads: remember the milk
the shortcut now dangles: its target name no longer exists
two links pointing at each other: ELOOP
a hard link to a directory is refused
```

The model reproduces the behaviour of the real file system, and that was *tested*: the same random sequences of operations (creating directories and files, writing, reading, hard links, symbolic links, removing files and directories, listing, and reading links, with deliberately awkward cases such as dangling and looping links) were run both on `MiniFS` and in a temporary folder on the Mac used for this module, and after every single operation the two were compared, both the result or the kind of error and the whole visible state (what exists, what it contains, how many names each file has, and which names share an inode). They agreed on all 60,000 operations in 1,000 random sessions. The one exception that had to be excluded is removing a directory with `unlink` or hard-linking one, for which different operating systems report different errors.

On the real system, the refused hard link to a directory looks like this:

```python
with tempfile.TemporaryDirectory() as workshop:
    os.mkdir(os.path.join(workshop, "sub"))
    try:
        os.link(os.path.join(workshop, "sub"), os.path.join(workshop, "alias"))
    except OSError as error:
        print("hard link to a directory on this machine:", errno.errorcode[error.errno])
    print("a name that differs only in capital letters refers to the same file:", end=" ")
    with open(os.path.join(workshop, "readme.txt"), "w") as handle:
        handle.write("x")
    print(os.path.exists(os.path.join(workshop, "README.TXT")))
```

One run on the test machine printed:

```
hard link to a directory on this machine: EPERM
a name that differs only in capital letters refers to the same file: True
```

The last line depends on the volume. The default format of macOS is **case-insensitive but case-preserving**, so `README.TXT` and `readme.txt` are the same file, whereas the usual Linux formats are case-sensitive and would print `False`. Code that moves between systems must not rely on either behaviour.

## 🗂️ Directory Structures

Directory designs have grown from simple to general: a **single-level** directory with one flat list of names (every name must be unique); a **two-level** directory with one list per user; the **tree**, where directories contain directories, so that every file has one place and one path; and the **graph**, where hard links let a file appear in several directories (an acyclic graph, as long as hard links to directories are forbidden) and symbolic links can point anywhere, which allows cycles, and needs the loop limit above. The tree is a convenient default, the graph is what you get as soon as you create a link, and the cost of the graph is that a file no longer has a single "real" path.

## Common Misconceptions

- **"A file's name is part of the file."** The name lives in a directory; the file's metadata and data are reached through an inode. Renaming changes a directory entry and nothing else.
- **"Deleting a file erases it."** It removes a name. The data is freed only when the last name is gone and the last open descriptor is closed, and even then it is usually not overwritten, only made available for reuse.
- **"A symbolic link is a kind of hard link."** A hard link is another name for the same inode, and is indistinguishable from the original. A symbolic link is a separate small file that holds a path, and can dangle.
- **"Two `open` calls on the same file share a position."** Each `open` has its own offset; only descriptors made by `dup` or inherited through `fork` share one.
- **"Paths are just strings."** Resolving one involves permissions on every directory along the way, symbolic links, and limits, and the same string can mean different things on different volumes (case sensitivity) or at different times (links can be changed).

## ➡️ Next

Continue to [file-allocation.md](file-allocation.md): how the file system decides which blocks hold a file's data, with three classic methods (contiguous, linked, and indexed), and the modern one that has largely replaced them, extents.
