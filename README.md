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
git clone https://github.com/D1533/syscall-info.git
cd syscall-info
```

---

## Usage
```bash
$ python3 syscallinfo.py [syscall] [--all] [--arch ARCH] [--asm] [--json]

```
`syscall`         - Syscall name or number  
`--all`           - Print full syscall table  
`--arch ARCH`     - Select architecture (x86_64 default, or x86)  
`--asm`           - Generate assembly syscall stub  
`--json`          - Output syscall information in JSON format 

---

## Examples

### Search by syscall name
```bash
$ python3 syscallinfo.py read
```
```text
read
  rax: 0
  rdi: unsigned int fd
  rsi: char *buf
  rdx: size_t count
```
### Search by syscall number
```bash
$ python3 syscallinfo.py 0
```
```text
read
  rax: 0
  rdi: unsigned int fd
  rsi: char *buf
  rdx: size_t count
```

### Dump all syscall table
```bash
$ python3 syscallinfo.py --all
```
```text
0 read(unsigned int fd, char *buf, size_t count)
1 write(unsigned int fd, const char *buf, size_t count)
2 open(const char *filename, int flags, int mode)
3 close(unsigned int fd)
...
```

### Get ASM model code
```bash
$ python3 syscallinfo.py read --asm
```
```text
; read syscall
mov rax, 0
mov rdi, fd      ; unsigned int fd
mov rsi, buf     ; char *buf
mov rdx, count   ; size_t count
syscall
```

### Get JSON format
```bash
$ python3 syscallinfo.py read --json
```
```text
{
  "number": 0,
  "name": "read",
  "args": [
    "unsigned int fd",
    "char *buf",
    "size_t count"
  ],
  "registers": [
    "rdi",
    "rsi",
    "rdx"
  ],
  "syscall_reg": "rax",
  "syscall_instr": "syscall",
  "arch": "x86_64"
}
```
