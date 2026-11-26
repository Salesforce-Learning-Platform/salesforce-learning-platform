# 🔐 File Permissions and Access Control

## Who May Do What to Which File?

A file system keeps the files of many users and programs on one device, so for every request it must decide whether *this* process may do *this* to *that* file. Typically a file system keeps permission settings for each file and directory that grant or deny the ability to manipulate it, often by function (read, change, navigate, execute) and for different users and groups of users ([Wikipedia: File-system permissions](https://en.wikipedia.org/wiki/File-system_permissions)). Two technologies dominate: the traditional permission bits that Unix introduced and POSIX later standardized, and **access control lists**, which exist in several variants (the same article). The checks run inside the kernel, in the system call, so a program cannot skip them (see [kernel-and-user-mode.md](../introduction-to-operating-systems/kernel-and-user-mode.md)).

In the abstract, the rights of every *subject* (a user or a process) over every *object* (a file) form a table, the **access control matrix**, introduced by Butler Lampson in 1971: each column is the access control list of one object, and each row is the access profile of one subject ([Wikipedia: Access control matrix](https://en.wikipedia.org/wiki/Access_control_matrix)). Storing the whole table would be wasteful, so real systems store a compressed form of it. Early Unix could afford about nine bits per file for the purpose ([OSTEP: Access Control](https://pages.cs.wisc.edu/~remzi/OSTEP/security-access.pdf)), and that budget is where the three classes of three bits each, described next, come from.

This file starts with the permission bits and their rules, follows them through default modes, opening, and directories, and then covers the special bits and access control lists. The next lesson, [file-system-security.md](file-system-security.md), turns to two ways of getting around permissions that are set correctly (races between a check and the use of its result, and path traversal) and to protections that do not rely on permissions at all (integrity checks, disk encryption, and least privilege). All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) as an ordinary user. That matters: a process with *appropriate privileges*, in practice the superuser, is granted read, write, and search access whatever the bits say, and execute access if at least one execute bit is set ([POSIX.1-2024, section 4.7](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html)), so the experiments below would show nothing when run as root. Machine-dependent results are labelled.

## 🔢 The Nine Permission Bits

Every file records an owner and a group as numbers (`st_uid` and `st_gid`, from the table in [files-and-directories.md](files-and-directories.md)), and nine **permission bits**: read, write, and execute for each of three **classes**: the file's *owner*, the members of the file's *group*, and *everybody else* (*other*). `stat.filemode` writes the bits as `rwxr-xr--`; the same bits in octal are `0o754`, where each digit is one class and read is worth 4, write 2, and execute 1. The bits mean different things on files and on directories:

| Bit | Worth | On a regular file | On a directory |
|-----|-------|-------------------|----------------|
| **r** | 4 | read the contents | list the names inside it |
| **w** | 2 | change the contents | add, remove, or rename entries (only together with **x**) |
| **x** | 1 | run it as a program | *search*: use the directory in a path to reach what is inside it |

A check never mixes classes. The kernel puts the requesting process in exactly one of them: the **owner class** if the process's effective user ID equals the file's owner; otherwise the **group class** if its effective group ID or one of its supplementary group IDs equals the file's group; otherwise the **other class** (the definitions of the three classes in [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap03.html)). Only the three bits of that one class are consulted: access is granted if the requested bit is set for the class to which the process belongs (POSIX.1-2024, section 4.7). The whole rule fits in a few lines:

```python
import os
import stat
import tempfile

READ, WRITE, EXECUTE = 4, 2, 1

def allowed(mode, owner, group, uid, groups, want):
    """May a process with user id `uid` and group ids `groups` do `want` (READ, WRITE, EXECUTE, or a sum of them)
    to a file with permission bits `mode`, owner id `owner`, and group id `group`? (Ordinary users: root is exempt.)"""
    if uid == owner:
        granted = (mode >> 6) & 7        # the owner class decides, and nothing else is consulted
    elif group in groups:
        granted = (mode >> 3) & 7        # not the owner, but in the file's group: the group class decides
    else:
        granted = mode & 7               # everybody else
    return granted & want == want

ADA, LIN, EVE = 1001, 1002, 1003         # three invented users; ada owns the files; ada and lin are in group 50
for mode in (0o640, 0o604):
    print(stat.filemode(mode | stat.S_IFREG), "owned by ada, group 50")
    for name, uid, groups in (("ada", ADA, {50}), ("lin", LIN, {50}), ("eve", EVE, {99})):
        rights = "".join(letter if allowed(mode, ADA, 50, uid, groups, bit) else "-"
                         for letter, bit in (("r", READ), ("w", WRITE), ("x", EXECUTE)))
        print(f"   {name} gets {rights}")
```

```text
-rw-r----- owned by ada, group 50
   ada gets rw-
   lin gets r--
   eve gets ---
-rw----r-- owned by ada, group 50
   ada gets rw-
   lin gets ---
   eve gets r--
```

Look at the second file. lin is a member of the file's group, so only the group bits count for lin, and they are `---`: lin is refused, although a complete stranger (eve) may read. The class that applies is the most specific one, not the most generous.

Is the model right? The block below tries all 512 combinations of the nine bits on a file that the process owns, asks the operating system about every non-empty mix of read, write, and execute with `os.access`, and also really opens the file for reading, for writing, and for both:

```python
me = os.getuid()
my_groups = set(os.getgroups()) | {os.getgid()}

cases = disagreements = 0
with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "probe")
    open(path, "w").close()
    info = os.stat(path)
    for mode in range(0o1000):                                     # all 512 combinations of the nine bits
        os.chmod(path, mode)
        for want in range(1, 8):                                   # r, w, x, rw, rx, wx, rwx
            flags = (os.R_OK if want & READ else 0) | (os.W_OK if want & WRITE else 0) | (os.X_OK if want & EXECUTE else 0)
            cases += 1
            disagreements += os.access(path, flags) != allowed(mode, info.st_uid, info.st_gid, me, my_groups, want)
        for open_flags, want in ((os.O_RDONLY, READ), (os.O_WRONLY, WRITE), (os.O_RDWR, READ | WRITE)):
            try:
                os.close(os.open(path, open_flags))
                opened = True
            except PermissionError:
                opened = False
            cases += 1
            disagreements += opened != allowed(mode, info.st_uid, info.st_gid, me, my_groups, want)
    os.chmod(path, 0o600)
print(f"{cases} requests checked; the model and the operating system disagreed on {disagreements}")
```

```text
5120 requests checked; the model and the operating system disagreed on 0
```

Because the test file belongs to the process, this exercises only the owner class; the group and other classes were compared with the operating system on files owned by other users, as described at the end of this file. The most surprising consequence of the rule can be seen directly. The owner class decides for the owner even when it is the *least* generous:

```python
with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "note.txt")
    open(path, "w").close()
    for mode in (0o700, 0o070, 0o007, 0o077):
        os.chmod(path, mode)
        try:
            os.close(os.open(path, os.O_RDONLY))
            outcome = "opened"
        except PermissionError:
            outcome = "permission denied"
        print(f"{stat.filemode(mode | stat.S_IFREG)} on a file I own: {outcome}")
    os.chmod(path, 0o600)              # the owner can always change the mode, whatever it is
```

```text
-rwx------ on a file I own: opened
----rwx--- on a file I own: permission denied
-------rwx on a file I own: permission denied
----rwxrwx on a file I own: permission denied
```

Nobody is locked out for good by this: changing a file's mode is a right of its owner, whatever the mode says, so a mistake like `0o070` is undone with one `chmod`.

## 🎭 Defaults: the umask

Programs rarely choose permission bits with care; they ask for something generous, such as `0o666` for a new file (Python's `open` does) or `0o777` for a new directory, and the system trims the request. Every process has a **umask**, a mask whose set bits are removed from the mode requested when a file or directory is created: the file gets `mode & ~umask` ([Linux man page: `open(2)`](https://man7.org/linux/man-pages/man2/open.2.html), [`umask(2)`](https://man7.org/linux/man-pages/man2/umask.2.html), and [Wikipedia: umask](https://en.wikipedia.org/wiki/Umask)). The typical default is octal `022`, which switches off write for the group and for others, so new files are `rw-r--r--` and new directories `rwxr-xr-x`. The mask belongs to the process and is passed on to the programs it starts, which is why the shell's `umask` command changes what everything launched from that shell creates:

```python
def mode_of(path):
    return stat.filemode(os.stat(path).st_mode)

with tempfile.TemporaryDirectory() as workshop:
    previous = os.umask(0o000)                    # os.umask installs a new mask and returns the old one
    try:
        for mask in (0o000, 0o022, 0o077):
            os.umask(mask)
            file_path = os.path.join(workshop, f"file-{mask:03o}")
            folder_path = os.path.join(workshop, f"folder-{mask:03o}")
            os.close(os.open(file_path, os.O_CREAT | os.O_WRONLY, 0o666))        # ask for rw-rw-rw-
            os.mkdir(folder_path, 0o777)                                         # ask for rwxrwxrwx
            print(f"umask {mask:03o}: file {mode_of(file_path)} | directory {mode_of(folder_path)}")
        os.umask(0o000)
        descriptor, private_file = tempfile.mkstemp(dir=workshop)
        os.close(descriptor)
        print("mkstemp, even with umask 000:", mode_of(private_file), "| mkdtemp:", mode_of(tempfile.mkdtemp(dir=workshop)))
    finally:
        os.umask(previous)                        # the mask is per process: always put it back
```

```text
umask 000: file -rw-rw-rw- | directory drwxrwxrwx
umask 022: file -rw-r--r-- | directory drwxr-xr-x
umask 077: file -rw------- | directory drwx------
mkstemp, even with umask 000: -rw------- | mkdtemp: drwx------
```

A umask can only *remove* permissions, so a program that creates something private should ask for what it needs and not rely on the mask it happened to inherit: `0o600` for a secret file, `0o700` for a private directory. The standard library does this for you: `tempfile.mkstemp` creates a file that is readable and writable only by the creating user, and `mkdtemp` a directory that only that user can read, write, or search ([Python docs: `tempfile`](https://docs.python.org/3/library/tempfile.html)). They ask for `0o600` and `0o700`, so even a umask of `000` cannot widen them, as the last line of the output shows.

## 🚪 Permissions Are Checked at Open Time

The permission check happens when a name is turned into an open file, in `open`, and not again on each `read` or `write` that follows. The descriptor *is* the result of the check, the open file description of [files-and-directories.md](files-and-directories.md), and it keeps working after the bits change:

```python
with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "diary.txt")
    with open(path, "w") as handle:
        handle.write("0123456789")
    reader = open(path, "rb")                       # the permission check happens here, once
    os.chmod(path, 0o000)                           # from now on nobody may open it, not even its owner
    print("mode now:", mode_of(path))
    print("the descriptor opened earlier still reads:", reader.read(4))
    try:
        open(path, "rb")
    except PermissionError as error:
        print("a new open fails:", error.strerror)
    reader.close()

    # The mode given to a creating open() governs later opens, not the call that creates the file:
    receipt = os.path.join(workshop, "receipt.txt")
    descriptor = os.open(receipt, os.O_CREAT | os.O_WRONLY, 0o400)      # ask for a read-only file ...
    print("wrote", os.write(descriptor, b"paid"), "bytes through the descriptor that created it")
    os.close(descriptor)
    try:
        os.open(receipt, os.O_WRONLY)
    except PermissionError as error:
        print("a later open for writing fails:", error.strerror)
```

```text
mode now: ----------
the descriptor opened earlier still reads: b'0123'
a new open fails: Permission denied
wrote 4 bytes through the descriptor that created it
a later open for writing fails: Permission denied
```

This has practical consequences. Taking permission away does not cut off a process that already has the file open, and a program that wants to revoke access must close the file or stop the process. A descriptor can also be *handed on*: a child created with `fork` inherits it (the experiment in [files-and-directories.md](files-and-directories.md)), and holding one is enough to use the file, whatever the bits say now. In that respect it resembles a **capability**, a communicable, unforgeable token of authority that refers to an object together with a set of access rights; Wikipedia observes that capabilities are used much like file descriptors, but for every kind of object ([Wikipedia: Capability-based security](https://en.wikipedia.org/wiki/Capability-based_security)). Finally, the mode passed to a creating `open` applies only to future opens: as the manual page notes, a call that creates a read-only file may well return a read/write descriptor ([`open(2)`](https://man7.org/linux/man-pages/man2/open.2.html)).

## 📁 Directory Permissions

A directory is a file whose contents are names, so its three bits describe what may be done with *names*: **r** lists them, **x** looks one up and passes through the directory on the way to something inside, and **w** changes the list, which is possible only together with **x**. The block below tries five operations on all eight combinations of the owner's bits of a directory that contains one file:

```python
def attempt(action):
    try:
        action()
        return "yes"
    except PermissionError:
        return "no"

print("bits    list names  look up a name  read a file  create  delete")
for bits in range(8):
    with tempfile.TemporaryDirectory() as workshop:
        folder = os.path.join(workshop, "folder")
        os.mkdir(folder)
        known = os.path.join(folder, "known.txt")
        with open(known, "w") as handle:
            handle.write("hello")
        os.chmod(folder, bits << 6)                                    # the owner class of the directory only

        def read():
            with open(known) as handle:
                handle.read()

        def create():
            os.close(os.open(os.path.join(folder, "new.txt"), os.O_CREAT | os.O_WRONLY, 0o600))

        letters = ("r" if bits & READ else "-") + ("w" if bits & WRITE else "-") + ("x" if bits & EXECUTE else "-")
        answers = (attempt(lambda: os.listdir(folder)), attempt(lambda: os.stat(known)), attempt(read),
                   attempt(create), attempt(lambda: os.unlink(known)))
        os.chmod(folder, 0o700)                                        # restore, so that the folder can be cleaned up
        print(f"{letters:<7} {answers[0]:<11} {answers[1]:<15} {answers[2]:<12} {answers[3]:<7} {answers[4]}")
```

```text
bits    list names  look up a name  read a file  create  delete
---     no          no              no           no      no
--x     no          yes             yes          no      no
-w-     no          no              no           no      no
-wx     no          yes             yes          yes     yes
r--     yes         no              no           no      no
r-x     yes         yes             yes          no      no
rw-     yes         no              no           no      no
rwx     yes         yes             yes          yes     yes
```

Read the table row by row. With **x** alone (`--x`) the names cannot be listed, but a file whose name is known can still be used: not listing a name is not protecting it. With **r** alone (`r--`) the names can be listed and nothing can be touched, because even looking up an entry needs **x**. Creating and deleting need **w** *and* **x** (`-wx`, `rwx`). The last column holds the point that surprises people most: to delete a file you need permission on the *directory* that contains it, and the file's own bits do not matter:

```python
with tempfile.TemporaryDirectory() as workshop:
    folder = os.path.join(workshop, "folder")
    os.mkdir(folder)
    locked = os.path.join(folder, "locked.txt")
    open(locked, "w").close()
    os.chmod(locked, 0o400)                              # a read-only file in a writable folder ...
    os.unlink(locked)
    print("read-only file in a writable folder deleted:", not os.path.exists(locked))

    open_file = os.path.join(folder, "open.txt")
    open(open_file, "w").close()                         # a writable file in a read-only folder ...
    os.chmod(folder, 0o500)
    with open(open_file, "w") as handle:
        handle.write("changed")
    print("writable file in a read-only folder: contents changed")
    for description, action in (("delete", lambda: os.unlink(open_file)),
                                ("rename", lambda: os.rename(open_file, os.path.join(folder, "renamed.txt")))):
        print(f"   {description}:", attempt(action))
    os.chmod(folder, 0o700)
```

```text
read-only file in a writable folder deleted: True
writable file in a read-only folder: contents changed
   delete: no
   rename: no
```

That leaves a problem for shared directories such as `/tmp`, where everybody must be able to create files: with the bits alone, anyone with write permission on the directory could also delete everyone else's files. The sticky bit, next, exists for exactly this.

## ⭐ Special Bits: setuid, setgid, and sticky

Three more bits sit in front of the nine and show up as `s` and `t` in a listing (they are defined in the manual page [`inode(7)`](https://man7.org/linux/man-pages/man7/inode.7.html) and described in Wikipedia's articles on [setuid and setgid](https://en.wikipedia.org/wiki/Setuid) and on the [sticky bit](https://en.wikipedia.org/wiki/Sticky_bit)):

- **setuid** (`4000`): on an executable file, the program runs with the effective user ID of the file's *owner*, not of the user who started it.
- **setgid** (`2000`): on an executable file, the same for the file's group; on a *directory*, new files and subdirectories inherit the directory's group instead of the creator's primary group, and new subdirectories inherit the bit too (this applies only to items created afterwards).
- **sticky** (`1000`): on a directory, only the file's owner, the directory's owner, or root may rename or delete a file in it. (On executable files it once kept a program in memory; that use is obsolete.)

Setuid and setgid let a user run an executable with the file system permissions of the executable's owner or group: they are used to give users *temporary, specific* privileges for a task that needs rights they do not normally have, such as changing a password stored in a system database, or sending and receiving the control packets of the `ping` command (the Wikipedia article on setuid). The effect applies only to binary executables, not to scripts, and many systems ignore the bit on shell scripts; the system usually also stops the invoking user from tampering with the privileged process, for example through `ptrace`, environment variables such as `PATH`, or signals (the same article). The sticky bit is the cure for the shared-directory problem above: it is typically set on `/tmp`, so users cannot delete or move each other's files. On your own machine they are easy to find:

```python
def special_programs(*folders):
    found, seen = [], set()
    for folder in folders:
        for entry in os.scandir(folder):
            info = entry.stat(follow_symlinks=False)
            identity = (info.st_dev, info.st_ino)
            if stat.S_ISREG(info.st_mode) and info.st_mode & (stat.S_ISUID | stat.S_ISGID) and identity not in seen:
                seen.add(identity)                # /bin may be another name for /usr/bin: list each file once
                found.append((entry.path, stat.filemode(info.st_mode), info.st_uid, info.st_gid))
    return sorted(found)

for path, mode, owner, group in special_programs("/usr/bin", "/bin", "/usr/sbin", "/sbin"):
    print(f"{path:<22} {mode}  owner {owner}  group {group}")
print("/tmp:", stat.filemode(os.stat("/tmp").st_mode))
```

One run on the test machine printed:

```
/bin/ps                -rwsr-xr-x  owner 0  group 0
/usr/bin/atq           -r-sr-xr-x  owner 0  group 0
/usr/bin/batch         -r-sr-xr-x  owner 0  group 0
/usr/bin/crontab       -rwsr-xr-x  owner 0  group 0
/usr/bin/login         -r-sr-xr-x  owner 0  group 0
/usr/bin/newgrp        -r-sr-xr-x  owner 0  group 0
/usr/bin/quota         -r-sr-xr-x  owner 0  group 0
/usr/bin/su            -rwsr-xr-x  owner 0  group 0
/usr/bin/sudo          -r-s--x--x  owner 0  group 0
/usr/bin/top           -r-sr-xr-x  owner 0  group 0
/usr/bin/write         -r-xr-sr-x  owner 0  group 4
/usr/sbin/postdrop     -rwxr-sr-x  owner 0  group 28
/usr/sbin/postqueue    -rwxr-sr-x  owner 0  group 28
/usr/sbin/traceroute   -r-sr-xr-x  owner 0  group 0
/usr/sbin/traceroute6  -r-sr-xr-x  owner 0  group 0
/tmp: drwxrwxrwt
```

An `s` in place of the owner's or group's `x` marks the bit, and the final `t` of `/tmp` is the sticky bit. Every program in the list holds its owner's authority while it reads arguments, environment variables, and file names supplied by whoever runs it. That is a **confused deputy** waiting to happen: a program tricked by another with fewer privileges into misusing its authority ([Wikipedia: Confused deputy problem](https://en.wikipedia.org/wiki/Confused_deputy_problem)). Wikipedia's original example is a compiler that was allowed to write into a system directory. A user asked it to put its debugging output in the file that held the billing records. The open succeeded, because the *compiler* had the right to write there, and the billing data was overwritten. Races and path traversal, in the next lesson, are two more ways of confusing a deputy, which is why the rule for setuid programs is to have few of them, keep them small, and treat every input as hostile.

## 📜 Access Control Lists

Three classes cannot say "ada may read, lin may read and write, everybody else nothing" unless someone creates a group for the purpose. An **access control list** (ACL) attaches to a file a list of entries, each naming a subject and the operations allowed to it; they were first implemented in the Multics file system in 1965 ([Wikipedia: Access-control list](https://en.wikipedia.org/wiki/Access-control_list)). POSIX ACLs on Linux add entries for individual users and groups to the owner, group, and other entries and are managed with `getfacl` and `setfacl` ([`acl(5)`](https://man7.org/linux/man-pages/man5/acl.5.html)); macOS uses richer lists whose entries can also *deny* operations. A Mac file has one ACL, an ordered list of entries, each referring to a user or a group and granting or denying a set of permissions ([macOS manual: `chmod`](https://keith.github.io/xcode-man-pages/chmod.1.html)). The experiment adds one entry that denies reading to everybody, using the macOS syntax:

```python
import subprocess
import sys

def acl_entries(path):
    """The entries `ls -le` prints below the line of a file (macOS)."""
    lines = subprocess.run(["ls", "-le", path], capture_output=True, text=True).stdout.splitlines()
    return [line.strip() for line in lines[1:]]

def owner_can_read(path):
    try:
        with open(path) as handle:
            handle.read()
        return True
    except PermissionError:
        return False

if sys.platform != "darwin":
    print("skipped: this demonstration uses the macOS syntax of chmod +a")
else:
    with tempfile.TemporaryDirectory() as workshop:
        path = os.path.join(workshop, "report.txt")
        with open(path, "w") as handle:
            handle.write("quarterly numbers")
        os.chmod(path, 0o644)
        for step, command in (("start", None), ("add an entry", ["chmod", "+a", "everyone deny read", path]),
                              ("remove the ACL", ["chmod", "-N", path])):
            if command:
                subprocess.run(command, check=True)
            print(f"{step:<15} mode {mode_of(path)} | ACL {acl_entries(path)} | owner can read: {owner_can_read(path)}")
```

```text
start           mode -rw-r--r-- | ACL [] | owner can read: True
add an entry    mode -rw-r--r-- | ACL ['0: group:everyone deny read'] | owner can read: False
remove the ACL  mode -rw-r--r-- | ACL [] | owner can read: True
```

The mode bits say that the owner may read the file in all three lines, yet in the second line the owner is refused: the ACL entry took part in the decision, and as a *deny* entry it overruled the bits. Entries can also grant what the bits withhold. On the test Mac the system log files in `/var/log/asl` are mode `rw-------` and owned by root, yet `ls -le` shows the entry `0: group:admin allow read` on them, so members of the `admin` group can read them. An ACL stores the matrix of the first section by columns, one list per object. Systems built on **capabilities** store it by rows instead, one list per subject, and the OSTEP chapter on [access control](https://pages.cs.wisc.edu/~remzi/OSTEP/security-access.pdf) compares the two designs.

## ✅ Checking the Code

Each piece of code was compared with an independent reference.

The permission model `allowed` was compared with the operating system in two ways. First, on a file that the process owns, for every one of the 512 mode values and every kind of request (the block in the section on the nine bits: 5,120 requests, no disagreement). Second, for the group and other classes, on every regular file and directory that could be examined under `/etc`, `/bin`, `/sbin`, `/usr/bin`, `/usr/sbin`, `/usr/lib`, `/usr/share`, `/var`, `/Library`, and `/System/Library/CoreServices` of the test Mac: about 170,000 objects, about 157,000 of them owned by other users, and about 468,000 requests for read, write, and execute access (write requests on read-only volumes were left out). The model and `os.access` agreed on all but 236 of them (99.95%; the exact counts drift as files come and go). The 236 exceptions are not faults of the rule. Twenty-two are files with an ACL entry that grants access (like the system logs of the ACL section), and the other 214 were refused by something beyond the mode bits: where I traced the refusals, the failing call returned `EPERM` ("operation not permitted") instead of `EACCES` ("permission denied"), and macOS adds protections of its own on top of the permission bits.

The rest of the code was checked like this. The umask formula `mode & ~umask` held for all 512 masks, and `mkstemp` and `mkdtemp` never produced a group or other bit. The directory table agreed with its rule (**r** lists, **x** looks up and reads, **w** together with **x** creates and deletes) for all 8 combinations.

## Common Misconceptions

- **"`chmod 777` is a harmless way to make a permission error go away."** It lets every user on the machine change the file, and on a directory without the sticky bit it lets them delete other people's files. A permission error usually means that the wrong user or group owns the file, and that is what should be fixed.
- **"The owner always has at least as much access as everybody else."** Only one class is consulted: with mode `0o070` the owner is refused while the group has full access (the owner can still change the mode back).
- **"Taking permission away cuts off a program that already has the file open."** The check happens at open time, so a descriptor opened earlier keeps working until it is closed.
- **"Write permission on a file lets me delete it."** Deleting and renaming need write *and* search permission on the directory that holds the file; the file's own bits do not matter.
- **"A file whose name nobody can list is protected."** A directory with only search permission cannot be listed, but anyone who may enter it can open a file whose name they know; protection comes from the bits on the files themselves.

## ➡️ Next

Continue to [file-system-security.md](file-system-security.md): correct permissions are not the whole story, because programs act on names that other users can influence. The next lesson shows how a check can be raced, how a path can escape its folder, and what integrity checks, encryption, and least privilege add.
