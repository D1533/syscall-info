## syscall-info

A fast CLI tool to inspect Linux system calls and generate assembly syscall stubs for x86 and x86_64 architectures.

Designed for reverse engineering, CTFs, exploit development, and learning Linux internals.

---

## Features

- Lookup syscalls by **name or number**
- Supports **x86 and x86_64**
- Generate **assembly syscall stubs**
- JSON output for scripting and automation
- Dump full syscall tables
- Lightweight (no dependencies)

---

## Installation

```bash
git clone https://github.com/yourname/syscall-info.git
cd syscall-info
```

## Usage
```bash
python3 syscall.py [syscall] [--all] [--arch ARCH] [--asm] [--json]
```
