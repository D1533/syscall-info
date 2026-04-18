#!/usr/bin/env python3

import argparse
import json

ABI = {
    "x86": {
        "regs": ["ebx", "ecx", "edx", "esi", "edi", "ebp"],
        "syscall_instr": "int 0x80",
        "syscall_reg": "eax",
        "file": "syscalls/x86",
    },
    "x86_64": {
        "regs": ["rdi", "rsi", "rdx", "r10", "r8", "r9"],
        "syscall_instr": "syscall",
        "syscall_reg": "rax",
        "file": "syscalls/x86_64",
    }
}

class SyscallDB:
    def __init__(self, arch):
        self.arch = arch
        self.regs = ABI[arch]["regs"]
        self.syscall_instr = ABI[arch]["syscall_instr"]
        self.syscall_reg = ABI[arch]["syscall_reg"]
        self.file = ABI[arch]["file"]
        self.syscalls_by_num, self.syscalls_by_name = self._load_data()
    
    def _load_data(self):
        syscalls_by_num = {}
        syscalls_by_name = {}
        with open(self.file) as f:
            for line in f:
                line_data = line.strip().split(",")
                syscalls_by_num[line_data[0]] = line_data[1:]
                syscalls_by_name[line_data[1]] = [line_data[0]] + line_data[2:]

        return syscalls_by_num, syscalls_by_name
    
    def get_syscall_data(self, arg):
        if arg.isdigit():
            num = arg
            if num not in self.syscalls_by_num:
                return None
            data = self.syscalls_by_num[num]
            name = data[0]
            args = data[1:]
        else:
            name = arg
            if name not in self.syscalls_by_name:
                return None
            data = self.syscalls_by_name[name]
            num = data[0]
            args = data[1:]

        return {"number": int(num), 
                "name": name, 
                "args": args, 
                "registers": self.regs[:len(args)], 
                "syscall_reg": self.syscall_reg,
                "syscall_instr": self.syscall_instr,
                "arch": self.arch}

    def get_all_syscalls(self):
        return [self.get_syscall_data(num) for num in sorted(self.syscalls_by_num, key=lambda x: int(x))]


def print_all(data):
    for syscall in data:
        print(f"{syscall['number']} {syscall['name']}(" + ", ".join(syscall['args']) + ")")

def print_syscall(data, arg, json_output=False):
    if not data:
        print(f"Unknown syscall: {arg}")
        return

    if json_output:
        print(json.dumps(data, indent=2))
        return

    print(data["name"])
    print(f"  {data['syscall_reg']}: {data['number']}")
    for reg, arg in zip(data["registers"], data["args"]):
        print(f"  {reg}: {arg}")

def print_asm(data, arg):
    if not data:
        print(f"Unknown syscall: {arg}")
        return

    print(f"; {data['name']} syscall")
    print(f"mov {data['syscall_reg']}, {data['number']}")
    lines = []
    for reg, arg in zip(data["registers"], data["args"]):
        arg_name = arg.split()[-1].replace("*", "")
        instr = f"mov {reg}, {arg_name}"
        comment = arg
        lines.append((instr, comment))

    max_len = max((len(instr) for instr, _ in lines), default=0)
    for instr, comment in lines:
        print(f"{instr.ljust(max_len)}   ; {comment}")
    print(data['syscall_instr'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("syscall", nargs="?", help="syscall name or number")
    parser.add_argument("--all", action="store_true", help="print full syscall table")
    parser.add_argument("--arch", choices=["x86_64", "x86"], default="x86_64", help="select syscall architecture (default: 64-bit)")   
    parser.add_argument("--asm", action="store_true", help="generate assembly syscall stub")
    parser.add_argument("--json", action="store_true", help="output in JSON format")
    args = parser.parse_args()

    db = SyscallDB(args.arch)

    if args.all:
        data = db.get_all_syscalls()
        print_all(data)
    elif args.syscall:
        data = db.get_syscall_data(args.syscall)
        if args.asm:
            print_asm(data, args.syscall)
        else:
            print_syscall(data, args.syscall, args.json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


