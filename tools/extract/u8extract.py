"""Extract the translatable text of U8 usecode classes, in conversation order.

Read-only. Uses tools/diagnostics/u8dis.py for decoding.

For one usecode class it walks the code linearly and records:
  - barks with their runtime id (CLASS:IP of the calli), reconstructed as
    templates: literal text, {name} for getName(), {num} for numToStr(),
    {varXX} for string locals that act as parameters,
    {call_OOOO} for a string returned by a usecode function in the same class
  - text shown by Book::read, Scroll::read, Grave::read and Plaque::read
    (same id scheme: CLASS:IP of the calli)
  - options added to / removed from the answer list, and the answers the code
    compares with ("when answer is ..."); the latter also catch options that
    are added in ways the evaluator does not follow
  - values of parameter locals (param entries)

Parameter locals: a string local is treated as a placeholder when the values
assigned to it anywhere in the class are short words and/or the player's name
(e.g. ORLOK: getName() or "stranger "). Locals holding whole sentences that are
built up with concat are expanded instead.

The symbolic evaluator ignores control flow; that is sufficient for the
straight-line concat sequences U8 uses to build sentences.

Text is decoded from the game's code page (CP437); po_compile.py encodes the
English text back the same way.

Usage:
  python u8extract.py <class hex> [--flow out.txt] [--tsv out.tsv]
"""
import argparse, os, struct, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "diagnostics"))
import u8dis  # noqa: E402

GETNAME, NUMTOSTR, BARK, ASK = 0xBC, 0xB9, 0x49, 0x4A
READERS = {0x6E: "book", 0x6F: "scroll", 0x70: "grave", 0x71: "plaque"}
PARAM_MAX_LEN = 20   # longest literal still considered a parameter value
GAME_ENCODING = "cp437"

EVENT_NAMES = {0x00: "look", 0x01: "use (talk)", 0x02: "anim", 0x04: "cachein", 0x05: "hit",
               0x06: "gotHit", 0x07: "hatch", 0x08: "schedule", 0x09: "release", 0x0A: "equip",
               0x0B: "unequip", 0x0C: "combine", 0x0F: "calledFromAnim", 0x10: "enterFastArea",
               0x11: "leaveFastArea", 0x12: "cast", 0x13: "justMoved", 0x14: "AvatarStoleSomething",
               0x15: "guardianBark"}


def lit(b):
    return b.decode(GAME_ENCODING)


class Expr:
    """String expression: list of ('lit', text) / ('var', name) parts."""
    def __init__(self, parts):
        self.parts = parts

    def __add__(self, other):
        return Expr(self.parts + other.parts)

    def is_literal(self):
        return all(k == "lit" for k, _ in self.parts)

    def template(self):
        return "".join(v if k == "lit" else "{" + v + "}" for k, v in self.parts)

    def vars(self):
        return [v for k, v in self.parts if k == "var"]


def evaluate(rows, events, on_assign=None, params=None, emit=None, catalog=None, cls=0):
    """One linear pass of the symbolic evaluator (see module docstring).

    catalog rows: (kind, id, text, type, note)
    """
    params = params or {}
    locals_, stack = {}, []
    pending, retval, bark_arg, last_lit, cond = False, None, None, None, []
    where = ""        # flow position for notes: event and current answer condition

    def local_expr(off):
        # parameter locals may be read before (in code order) their assignment
        name = f"var{off:02X}"
        return Expr([("var", name)]) if name in params else locals_.get(off)

    for i, (pc, op, args, s) in enumerate(rows):
        if pc in events:
            ev = events[pc]
            where = f"event {ev:02X} ({EVENT_NAMES.get(ev, '?')})"
            if emit:
                emit("")
                emit(f"=== event {ev:02X} @ {pc:04X}")
            locals_.clear(); stack.clear(); pending = False

        if op == 0x0D:
            stack.append(Expr([("lit", lit(s))])); pending = True; last_lit = lit(s)
        elif op == 0x0F:
            fn = args[1] | (args[2] << 8)
            retval = {GETNAME: Expr([("var", "name")]),
                      NUMTOSTR: Expr([("var", "num")])}.get(fn)
            if (fn == BARK or fn in READERS) and emit:
                kind = "bark" if fn == BARK else READERS[fn]
                pid = f"{cls:04X}:{pc:04X}"
                label = kind.upper()
                if bark_arg is None:
                    emit(f"  {label:5} {pid}  <unresolved>")
                    catalog.append((kind, pid, "", "unresolved", where))
                else:
                    typ = "literal" if bark_arg.is_literal() else "template"
                    shown = bark_arg.template()
                    emit(f"  {label:5} {pid}  \"{shown if kind == 'bark' else shown[:70]}\"")
                    for v in bark_arg.vars():
                        if v in params:
                            emit(f"        {{{v}}} = " + " | ".join(sorted(params[v])))
                    catalog.append((kind, pid, shown, typ, where))
            if fn in (BARK, ASK) or fn in READERS:
                if fn == ASK and emit:
                    emit("  ASK   (player chooses)")
                bark_arg = None; stack.clear(); pending = False
        elif op == 0x11:                               # call usecode function
            off = struct.unpack_from("<H", args, 2)[0]
            retval = Expr([("var", f"call_{off:04X}")])
        elif op == 0x5E:
            # a usecode function's result only counts as a string when it is
            # concatenated right away (functions also return numbers)
            if retval is not None and (retval.vars()[0] in ("name", "num") or
                                       (i + 1 < len(rows) and rows[i + 1][1] == 0x16)):
                stack.append(retval); pending = True
        elif op == 0x16 and len(stack) >= 2:
            b = stack.pop(); a = stack.pop(); stack.append(a + b); pending = True
        elif op == 0x01 and pending and stack:        # pop string into local
            off = args[0]
            e = stack.pop(); pending = bool(stack)
            if on_assign:
                on_assign(off, e)
            name = f"var{off:02X}"
            locals_[off] = Expr([("var", name)]) if name in params else e
        elif op == 0x41:                               # push string local (copy)
            e = local_expr(args[0])
            if e is not None:
                stack.append(e); pending = True
        elif op == 0x69:                               # string local as pointer
            bark_arg = local_expr(args[0])
        elif op == 0x6B and stack:                     # string to pointer
            bark_arg = stack.pop(); pending = bool(stack)
        elif op == 0x0E and stack and last_lit is not None:  # one-element list
            stack.pop(); pending = False
            if emit:
                nxt = rows[i + 1][1] if i + 1 < len(rows) else None
                if nxt == 0x1A:
                    emit(f"  - option \"{last_lit}\"")
                else:
                    emit(f"  + option \"{last_lit}\"")
                    catalog.append(("ask", f"{cls:04X}", last_lit, "answer", where))
        elif op == 0x26:                               # strcmp
            if last_lit is not None:
                cond.append(last_lit)
            stack.clear(); pending = False
        elif op == 0x51 and cond:                      # jne closing a condition
            # skip the conversation loop's "answer != Goodbye" guard
            if not (cond == ["Goodbye. "] and rows[i - 1][1] == 0x30):
                header = " or ".join(f'"{c}"' for c in cond)
                where = where.split(", after")[0] + f", after {header}"
                if emit:
                    emit("")
                    emit("  when answer is " + header + ":")
                if catalog is not None:
                    for c in cond:
                        if c:
                            catalog.append(("ask?", f"{cls:04X}", c, "answer check", where))
            cond = []


def extract(cls, data=None, ents=None, names=None):
    """Returns (class name, flow lines, catalog rows, params).

    catalog rows: (kind, id, text, type, note); kind is bark, ask, book,
    scroll, grave, plaque or param.
    """
    if data is None:
        data, ents = u8dis.load_flex(u8dis.USECODE)
    if names is None:
        names = u8dis.class_names(data, ents)
    cd = u8dis.obj(data, ents, cls + 2)
    if len(cd) < 0x8C:
        return names.get(cls, "?"), [], [], {}
    rows = list(u8dis.disasm(cd[0x0C:]))
    events = {}
    for e in range(32):
        off = struct.unpack_from("<I", cd, 12 + 4 * e)[0]
        if off:
            events[off] = e

    # pass 1: every value assigned to each string local
    assigned = {}
    evaluate(rows, events, on_assign=lambda off, e: assigned.setdefault(off, []).append(e))
    params = {}
    for off, vals in assigned.items():
        simple = all(len(v.parts) == 1 and (v.vars() == ["name"] or
                     (v.is_literal() and len(v.template()) <= PARAM_MAX_LEN)) for v in vals)
        if simple and len({v.template() for v in vals}) > 1:
            params[f"var{off:02X}"] = {('"' + v.template() + '"') if v.is_literal() else "{name}"
                                       for v in vals}

    # pass 2: emit flow + catalog
    flow, catalog = [], []
    evaluate(rows, events, params=params, emit=flow.append, catalog=catalog, cls=cls)

    has_ask = any(op == 0x0F and (args[1] | (args[2] << 8)) == ASK for _, op, args, _ in rows)
    seen, cat = set(), []
    for kind, pid, text, typ, note in catalog:
        if kind == "ask?":
            # compared answers count only in classes that ask
            if not has_ask:
                continue
            kind = "ask"
        if kind == "ask":                    # same class + text = same answer
            if (kind, pid, text) in seen:
                continue
            seen.add((kind, pid, text))
        cat.append((kind, pid, text, typ, note))

    used = {v for _, _, text, _, _ in cat for v in Expr([("lit", text)]).template().split("{")[1:]}
    for v, vals in sorted(params.items()):
        if not any(f"{{{v}}}" in r[2] for r in cat):
            continue
        for x in sorted(vals):
            if x.startswith('"'):
                cat.append(("param", f"{cls:04X}:{v}", x[1:-1], "param-value",
                            f"value of {{{v}}}: " + " | ".join(sorted(vals))))
    return names.get(cls, "?"), flow, cat, params


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls")
    ap.add_argument("--flow")
    ap.add_argument("--tsv")
    a = ap.parse_args()
    cls = int(a.cls, 16)
    name, flow, cat, params = extract(cls)

    text = "\n".join([f"# {name} (class {cls:04X}) - conversation flow from EUSECODE.FLX"] + flow) + "\n"
    if a.flow:
        open(a.flow, "w", encoding="utf-8", newline="\n").write(text)
    else:
        sys.stdout.write(text)

    if a.tsv:
        with open(a.tsv, "w", encoding="utf-8", newline="\n") as f:
            f.write("# kind\tid\tenglish (template)\ttype\tnote\n")
            for kind, pid, eng, typ, note in cat:
                f.write(f"{kind}\t{pid}\t{eng}\t{typ}\t{note}\n")

    count = lambda k: sum(r[0] == k for r in cat)
    nt = sum(r[3] == "template" for r in cat)
    nu = sum(r[3] == "unresolved" for r in cat)
    print(f"[{name}] barks={count('bark')} (templates={nt}, unresolved={nu}) answers={count('ask')} "
          f"books={count('book')} scrolls={count('scroll')} graves={count('grave')} "
          f"plaques={count('plaque')} params={count('param')}", file=sys.stderr)


if __name__ == "__main__":
    main()
