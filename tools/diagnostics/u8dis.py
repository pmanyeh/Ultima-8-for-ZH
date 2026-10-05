"""Read-only U8 usecode research disassembler (Phase 1).

Operand sizes derived from scummvm-src/engines/ultima/ultima8/usecode/uc_machine.cpp
(execProcess). Class layout from usecode_flex.cpp / usecode.cpp:
  flex object (classid + 2) = class data; code base offset = 0x0C;
  event table: uint32 at data[12 + 4*event] (U8, 32 events), relative to base.
  flex object 1 = class names, 13 bytes each starting at +4.
  The event table occupies the first 0x80 bytes after base, so code starts at 0x80.
  In U8, opcode 0x79 is a 1-byte end-of-function marker after `ret` (never executed);
  ScummVM's 2-byte 0x79 handler applies to Crusader only.

Offsets printed are relative to base, matching ScummVM's trace output (CLASS:IP).
Validation: `stats` must report desync=0 (English Gold Edition: 515 classes, 11238 strings).

Usage:
  python u8dis.py find <name>       list classes whose name contains <name>
  python u8dis.py events <class>    event entry points (class in hex)
  python u8dis.py dis <class>       disassemble a class
  python u8dis.py grepstr <text>    find push-string literals containing <text>
  python u8dis.py stats             decode every class and report desync

Set U8_USECODE to point at another EUSECODE.FLX.
"""
import os, struct, sys

USECODE = os.environ.get("U8_USECODE",
                         r"D:\git\Ultima 8 for ZH\Ultima 8\ENGLISH\USECODE\EUSECODE.FLX")

# opcode -> fixed operand byte count (0x0D handled specially)
SIZES = {0x00:1,0x01:1,0x02:1,0x03:2,0x08:0,0x09:3,0x0A:1,0x0B:2,0x0C:4,0x0E:2,0x0F:3,
         0x11:4,0x12:0,0x13:0,0x14:0,0x15:0,0x16:0,0x17:0,0x19:1,0x1A:1,0x1B:1}
for o in range(0x1C, 0x38): SIZES[o] = 0
SIZES.update({0x38:2,0x39:0,0x3A:0,0x3B:0,0x3C:0,0x3D:0,0x3E:1,0x3F:1,0x40:1,0x41:1,0x42:2,
              0x43:1,0x44:2,0x45:2,0x4B:1,0x4C:1,0x4D:1,0x4E:3,0x4F:3,0x50:0,0x51:2,0x52:2,
              0x53:0,0x54:2,0x57:6,0x58:8,0x59:0,0x5A:1,0x5B:2,0x5C:11,0x5D:0,0x5E:0,0x5F:0,
              0x60:0,0x61:0,0x62:1,0x63:1,0x64:1,0x65:1,0x66:1,0x67:1,0x69:1,0x6B:0,0x6C:2,
              0x6D:0,0x6E:1,0x6F:1,0x70:3,0x73:0,0x74:1,0x75:4,0x76:4,0x77:0,0x78:0,0x79:0,0x7A:0})

NAMES = {0x0D:"push_str",0x0E:"mklist",0x0F:"calli",0x11:"call",0x16:"str_concat",0x17:"list_add",
         0x19:"slist_union",0x1A:"slist_sub",0x26:"strcmp",0x50:"ret",0x51:"jne",0x52:"jmp",
         0x54:"implies",0x5B:"line",0x5C:"symbol",0x6C:"param_pid_change",0x6D:"push_proc_result",
         0x79:"end_func(U8)",0x7A:"end",0x0B:"push16",0x0A:"push8",0x0C:"push32",0x12:"pop_tmp",0x53:"suspend",
         0x57:"spawn",0x58:"spawn_inline",0x24:"eq16",0x2B:"not",0x75:"foreach_list",0x76:"foreach_slist",
         0x73:"loopnext",0x70:"loop",0x01:"pop16",0x40:"push_local16",0x3F:"push_local16",
         0x3E:"push_local8",0x4B:"push_addr",0x38:"in_list"}

INTR = {0x49:"Item::bark(str)",0x4A:"Item::ask(slist)",0x6E:"Book::read",0x6F:"Scroll::read",
        0x70:"Grave::read",0x71:"Plaque::read",0xB9:"numToStr",0xBC:"getName"}


def load_flex(path):
    data = open(path, "rb").read()
    count = struct.unpack_from("<I", data, 0x54)[0]
    ents = [struct.unpack_from("<II", data, 0x80 + 8 * i) for i in range(count)]
    return data, ents


def obj(data, ents, i):
    off, size = ents[i]
    return data[off:off + size]


def class_names(data, ents):
    names = obj(data, ents, 1)
    n = (len(names) - 4) // 13
    out = {}
    for c in range(n):
        raw = names[4 + 13 * c: 4 + 13 * c + 13].split(b"\0")[0]
        if raw:
            out[c] = raw.decode("latin-1")
    return out


def disasm(code):
    """Linear sweep. Yields (offset, opcode, operand bytes, string|None)."""
    pc = 0x80  # skip U8 event table (32 x uint32)
    while pc < len(code):
        op = code[pc]
        if op == 0x0D:
            ln = struct.unpack_from("<H", code, pc + 1)[0]
            s = code[pc + 3: pc + 3 + ln]
            yield pc, op, code[pc + 1: pc + 3], s
            pc += 3 + ln + 1
            continue
        if op not in SIZES:
            yield pc, op, b"", "!!UNKNOWN OPCODE - desync"
            return
        n = SIZES[op]
        yield pc, op, code[pc + 1: pc + 1 + n], None
        pc += 1 + n


def fmt(pc, op, args, s):
    name = NAMES.get(op, f"op{op:02X}")
    if op == 0x0D:
        return f"{pc:04X}: {name:<16} \"{s.decode('latin-1')}\""
    if op == 0x0F:
        nb, fn = args[0], struct.unpack_from("<H", args, 1)[0]
        return f"{pc:04X}: {name:<16} {fn:04X} {INTR.get(fn, '')} ({nb} arg bytes)"
    if op == 0x11:
        c, o = struct.unpack_from("<HH", args)
        return f"{pc:04X}: {name:<16} class {c:04X} event/offset {o:04X}"
    if op in (0x51, 0x52):
        rel = struct.unpack_from("<h", args)[0]
        return f"{pc:04X}: {name:<16} -> {pc + 3 + rel:04X}"
    return f"{pc:04X}: {name:<16} {args.hex(' ')}"


def main():
    data, ents = load_flex(USECODE)
    names = class_names(data, ents)
    cmd = sys.argv[1]
    if cmd == "find":
        pat = sys.argv[2].upper()
        for c, n in names.items():
            if pat in n.upper():
                print(f"class {c:04X} ({c})  {n}  size={ents[c + 2][1]}")
    elif cmd == "events":
        c = int(sys.argv[2], 16)
        cd = obj(data, ents, c + 2)
        for e in range(32):
            off = struct.unpack_from("<I", cd, 12 + 4 * e)[0]
            if off:
                print(f"event {e:02X}: {off:04X}")
    elif cmd == "dis":
        c = int(sys.argv[2], 16)
        code = obj(data, ents, c + 2)[0x0C:]
        for row in disasm(code):
            print(fmt(*row))
    elif cmd == "grepstr":
        pat = sys.argv[2].encode("latin-1")
        for c in names:
            code = obj(data, ents, c + 2)[0x0C:]
            if not code:
                continue
            for pc, op, args, s in disasm(code):
                if op == 0x0D and pat.lower() in s.lower():
                    print(f"{names[c]} {c:04X}:{pc:04X}  \"{s.decode('latin-1')}\"")
    elif cmd == "stats":
        tot = desync = strs = 0
        for c in names:
            code = obj(data, ents, c + 2)[0x0C:]
            if not code:
                continue
            tot += 1
            last = None
            for row in disasm(code):
                last = row
                if row[1] == 0x0D:
                    strs += 1
            if last and isinstance(last[3], str):
                desync += 1
                print(f"desync: {names[c]} {c:04X} at {last[0]:04X} op {last[1]:02X}")
        print(f"classes={tot} desync={desync} push_str={strs}")


if __name__ == "__main__":
    main()
