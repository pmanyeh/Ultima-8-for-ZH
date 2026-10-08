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

The conversation flow (and answers, notes) comes from one linear pass that
ignores control flow. The sentences of each bark / reader call site come from
a second pass that follows the branches (site_variants), so a sentence built
in pieces gets one entry per possible result, e.g. ERTHREAG
"{num} vial of blood" / "{num} vials of blood" / "{num} pile of wood" ...
Simple conditions ("x == 3", "hour() == 2") are tracked to skip impossible
paths. Call sites whose pieces combine into too many sentences are described
by hand in PART_TEMPLATES instead: the varying pieces become {partN}
placeholders with their own param entries (like {varXX}).

Text is decoded from the game's code page (CP437); po_compile.py encodes the
English text back the same way.

Usage:
  python u8extract.py <class hex> [--flow out.txt] [--tsv out.tsv]
"""
import argparse, collections, os, re, struct, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "diagnostics"))
import u8dis  # noqa: E402

GETNAME, NUMTOSTR, BARK, ASK = 0xBC, 0xB9, 0x49, 0x4A
READERS = {0x6E: "book", 0x6F: "scroll", 0x70: "grave", 0x71: "plaque"}
PARAM_MAX_LEN = 20   # longest literal still considered a parameter value
GAME_ENCODING = "cp437"

# Call sites whose sentences are combinations of independent pieces (too many
# to list one by one). Every sentence the code can build must match one of the
# templates (most literal text wins, as in the engine) or the "skip" pattern;
# the texts matched by each {partN} become "param CCCC:partN" entries.
PART_TEMPLATES = {
    # FIREITEM: item kind x spell x charges (singular / plural / none).
    # skip: the code's fall-through cases, an item without kind or spell
    (0x018D, 0x0462): {"templates": ["{part1}of {part2}with {num} use remaining",
                                     "{part1}of {part2}with {num} uses remaining",
                                     "{part1}of {part2}"],
                       "skip": r"^of |of (with |$)"},
    # time focus: hour x weekday x month
    (0x0596, 0x0B87): {"templates": ["Also it reads that the hour is currently  {part1},  "
                                     "the day is  {part2}, the {num} day of the month of {part3}. "]},
}
PART_RE = re.compile(r"\{part[0-9]+\}")
PART_MAX_VARIANTS = 2000   # sentences enumerated to check a PART_TEMPLATES site
PART_MAX_STATES = 1024

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


def evaluate(rows, events, on_assign=None, params=None, emit=None, catalog=None, cls=0,
             variants=None):
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
                if variants and pc in variants:
                    for n, text in enumerate(variants[pc]):
                        typ = "template" if "{" in text else "literal"
                        shown = text if kind == "bark" else text[:70]
                        emit(f"  {label if n == 0 else '|':5} {pid if n == 0 else '':9}  \"{shown}\"")
                        catalog.append((kind, pid, text, typ, where))
                    for v in sorted(params):
                        if any(f"{{{v}}}" in t for t in variants[pc]):
                            emit(f"        {{{v}}} = " + " | ".join(sorted(params[v])))
                elif bark_arg is None:
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
            # answers built with the player's name ("I am {name}.") are
            # sentence templates in the list
            if emit:
                for e in stack[-args[1]:]:
                    if not e.is_literal() and "name" in e.vars():
                        emit(f"  + option \"{e.template()}\"")
                        catalog.append(("ask", f"{cls:04X}", e.template(), "template", where))
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


MAX_STATES_PER_PC = 64     # distinct evaluator states explored at one instruction
MAX_VARIANTS = 64          # sentence variants kept for one call site
MAX_FACTS_PER_STATE = 8    # condition sets explored with the same string state
UNKNOWN = (("unknown", ""),)  # string value left by a previous loop iteration
CMP_OPS = {0x24: "eq", 0x28: "lt", 0x2A: "le", 0x2C: "gt", 0x2E: "ge"}  # 16 bit compares


def site_variants(rows, params, cls, max_states=MAX_STATES_PER_PC, max_variants=MAX_VARIANTS):
    """Every sentence each bark / reader call site can show, following branches.

    Same string semantics as evaluate(), but jne / foreach explore both
    successors. Paths whose string state is the same at an instruction are
    explored once, so the work stays proportional to the string values that
    really differ (e.g. ERTHREAG: quantity + "vial"/"vials" + " of blood").

    Returns ({calli pc: [template, ...] in discovery order}, {pc that hit a limit},
             {function start: [string it returns, ...]}).
    """
    index = {pc: i for i, (pc, _, _, _) in enumerate(rows)}
    starts = [rows[0][0]] if rows else []
    for i, (pc, op, args, _) in enumerate(rows):
        if op == 0x79 and i + 1 < len(rows):
            starts.append(rows[i + 1][0])             # next function
        elif op == 0x58:                              # spawn inline
            c, off, delta = struct.unpack_from("<HHH", args)
            if c == cls and off + delta in index:
                starts.append(off + delta)

    def local_expr(locals_, off):
        name = f"var{off:02X}"
        return (("var", name),) if name in params else locals_.get(off)

    def condition(i):
        """(symbol, comparison, constant) tested by the jne at rows[i], or None.

        symbol: a numeric local, or the result of a usecode function (assumed
        to return the same value within one path, e.g. the hour of the day).
        """
        def symbol(j):
            if j < 0:
                return None
            if rows[j][1] in (0x3F, 0x40):
                return ("local", rows[j][2][0])
            if rows[j][1] == 0x5E and j >= 1 and rows[j - 1][1] == 0x11:
                return ("call", bytes(rows[j - 1][2]))
            return None

        if i >= 3 and rows[i - 1][1] in CMP_OPS and rows[i - 2][1] in (0x0A, 0x0B):
            sym = symbol(i - 3)
            fmt_ = "<b" if rows[i - 2][1] == 0x0A else "<h"
            n = struct.unpack_from(fmt_, rows[i - 2][2])[0]
            return (sym, CMP_OPS[rows[i - 1][1]], n) if sym else None
        if i >= 2 and rows[i - 1][1] == 0x30:            # if (not x)
            sym = symbol(i - 2)
            return (sym, "eq", 0) if sym else None
        sym = symbol(i - 1)                              # if (x)
        return (sym, "ne", 0) if sym else None

    def with_fact(facts, sym, cmp, n, holds):
        """facts with "sym cmp n" (or its negation) added; None if impossible."""
        lo, hi, ex = dict(facts).get(sym, (-0x8000, 0x7FFF, frozenset()))
        if not holds:
            cmp = {"eq": "ne", "ne": "eq", "lt": "ge", "ge": "lt", "le": "gt", "gt": "le"}[cmp]
        if cmp == "eq":
            lo, hi = max(lo, n), min(hi, n)
        elif cmp == "ne":
            ex = ex | {n}
        elif cmp == "lt":
            hi = min(hi, n - 1)
        elif cmp == "le":
            hi = min(hi, n)
        elif cmp == "gt":
            lo = max(lo, n + 1)
        elif cmp == "ge":
            lo = max(lo, n)
        if lo > hi or (lo == hi and lo in ex):
            return None
        d = dict(facts)
        d[sym] = (lo, hi, frozenset(x for x in ex if lo <= x <= hi))
        return tuple(sorted(d.items()))

    def assigned_between(a, b):
        return frozenset(r[2][0] for r in rows[a:b + 1] if r[1] == 0x01)

    # a loop's back edge: string locals the loop assigns again hold a value of
    # the previous iteration, which the code normally does not show (UNKNOWN)
    loop_assigned = {}

    found, limited, returns = {}, set(), {}
    seen = collections.defaultdict(dict)   # pc -> string state -> facts seen
    for start in starts:
        work = [(index[start], (), (), False, None, None, ())]
        while work:
            i, locals_t, stack, pending, retval, bark_arg, facts = work.pop()
            while i < len(rows):
                pc, op, args, s = rows[i]
                key = (locals_t, stack, pending, retval, bark_arg)
                known = seen[pc].get(key)
                if known is None:
                    if len(seen[pc]) >= max_states:
                        limited.add(pc)
                        break
                    known = seen[pc][key] = set()
                if facts in known or len(known) >= MAX_FACTS_PER_STATE:
                    break
                known.add(facts)
                locals_ = dict(locals_t)
                nxt = [i + 1]
                if op == 0x0D:
                    stack += ((("lit", lit(s)),),); pending = True
                elif op == 0x0F:
                    fn = args[1] | (args[2] << 8)
                    retval = {GETNAME: (("var", "name"),), NUMTOSTR: (("var", "num"),)}.get(fn)
                    if fn == BARK or fn in READERS:
                        if bark_arg is not None and UNKNOWN[0] not in bark_arg:
                            t = Expr(list(bark_arg)).template()
                            lst = found.setdefault(pc, [])
                            if t not in lst:
                                if len(lst) < max_variants:
                                    lst.append(t)
                                else:
                                    limited.add(pc)
                    if fn in (BARK, ASK) or fn in READERS:
                        bark_arg = None; stack = (); pending = False
                elif op == 0x11:
                    off = struct.unpack_from("<H", args, 2)[0]
                    retval = (("var", f"call_{off:04X}"),)
                elif op == 0x5E:
                    if retval is not None and (retval[0][1] in ("name", "num") or
                                               (i + 1 < len(rows) and rows[i + 1][1] == 0x16)):
                        stack += (retval,); pending = True
                elif op == 0x16 and len(stack) >= 2:
                    stack = stack[:-2] + (stack[-2] + stack[-1],); pending = True
                elif op == 0x01 and pending and stack:
                    off = args[0]
                    e = stack[-1]; stack = stack[:-1]; pending = bool(stack)
                    name = f"var{off:02X}"
                    locals_[off] = (("var", name),) if name in params else e
                elif op == 0x41:
                    e = local_expr(locals_, args[0])
                    if e is not None:
                        stack += (e,); pending = True
                elif op == 0x69:
                    bark_arg = local_expr(locals_, args[0])
                elif op == 0x6B and stack:
                    bark_arg = stack[-1]; stack = stack[:-1]; pending = bool(stack)
                elif op == 0x0E and stack:
                    stack = stack[:-1]; pending = False
                elif op == 0x26:
                    stack = (); pending = False
                elif op == 0x12 and pending and stack:       # return a string
                    if UNKNOWN[0] not in stack[-1]:
                        t = Expr(list(stack[-1])).template()
                        lst = returns.setdefault(start, [])
                        if t not in lst:
                            lst.append(t)
                    stack = stack[:-1]; pending = bool(stack)
                elif op == 0x52:
                    target = pc + 3 + struct.unpack_from("<h", args)[0]
                    nxt = [index[target]] if target in index else []
                elif op == 0x51:
                    target = pc + 3 + struct.unpack_from("<h", args)[0]
                    cond = condition(i)
                    succ = [(i + 1, True), (index.get(target), False)]
                    nxt = []
                    for j, holds in succ:
                        if j is None:
                            continue
                        f = facts if cond is None else with_fact(facts, *cond, holds)
                        if f is not None:
                            nxt.append((j, f))
                elif op in (0x75, 0x76):
                    target = pc + 5 + struct.unpack_from("<h", args, 2)[0]
                    if target in index:
                        nxt.append(index[target])
                elif op in (0x50, 0x79, 0x7A):
                    nxt = []
                if op in (0x00, 0x01, 0x02) and ("local", args[0]) in dict(facts):
                    facts = tuple(x for x in facts if x[0] != ("local", args[0]))
                nxt = [x if isinstance(x, tuple) else (x, facts) for x in nxt]
                if any(j <= i for j, _ in nxt):
                    if i not in loop_assigned:
                        loop_assigned[i] = assigned_between(min(j for j, _ in nxt), i)
                    back = {off: UNKNOWN for off in loop_assigned[i] if off in locals_}
                else:
                    back = {}
                locals_t = tuple(sorted(locals_.items()))
                back_t = tuple(sorted({**locals_, **back}.items())) if back else locals_t
                if not nxt:
                    break
                # fall-through first: queue the other successors
                for j, f in nxt[1:]:
                    work.append((j, back_t if j <= i else locals_t, stack, pending, retval, bark_arg, f))
                if nxt[0][0] <= i:
                    locals_t = back_t
                i, facts = nxt[0]
    return found, limited, returns


def param_bark_sites(rows):
    """{function offset: [calli pc]}: functions that bark one of their
    parameters (e.g. METHOD 057C:087D barks the text its caller passes)."""
    out, start = {}, rows[0][0] if rows else 0
    for i, (pc, op, args, _) in enumerate(rows):
        if i and rows[i - 1][1] == 0x79:
            start = pc
        if op == 0x69 and args[0] < 0x80:       # positive BP offset: a parameter
            for j in range(i + 1, min(i + 4, len(rows))):
                r = rows[j]
                if r[1] == 0x0F and (r[2][1] | (r[2][2] << 8)) == BARK:
                    out.setdefault(start, []).append(r[0])
                    break
    return out


def passed_strings(rows, events):
    """[(class, function offset, text, note)]: string literals passed to a
    spawned or called usecode function (push_str + string-to-pointer)."""
    out, last, where = [], None, ""
    for i, (pc, op, args, s) in enumerate(rows):
        if pc in events:
            ev = events[pc]
            where = f"event {ev:02X} ({EVENT_NAMES.get(ev, '?')})"
        if op == 0x0D and i + 1 < len(rows) and rows[i + 1][1] == 0x6B:
            last = lit(s)
        elif op in (0x57, 0x11):                 # spawn / call
            c, o = struct.unpack_from("<HH", args, 2 if op == 0x57 else 0)
            if last is not None:
                out.append((c, o, last, where))
            last = None
        elif op == 0x0F and ((args[1] | (args[2] << 8)) in (BARK, ASK) or
                             (args[1] | (args[2] << 8)) in READERS):
            last = None
    return out


def class_rows(cls, data, ents):
    cd = u8dis.obj(data, ents, cls + 2)
    if len(cd) < 0x8C:
        return [], {}
    rows = list(u8dis.disasm(cd[0x0C:]))
    events = {}
    for e in range(32):
        off = struct.unpack_from("<I", cd, 12 + 4 * e)[0]
        if off:
            events[off] = e
    return rows, events


def part_match(tmpl, text):
    """Values of tmpl's {partN} placeholders in text, or None (shortest first,
    at least one character, as the engine matches templates)."""
    pieces = []
    pos = 0
    while True:
        a = tmpl.find("{part", pos)
        if a < 0:
            pieces.append(tmpl[pos:]); break
        b = tmpl.index("}", a)
        pieces += [tmpl[pos:a], tmpl[a + 1:b]]
        pos = b + 1

    def go(k, at, vals):
        lit_ = pieces[k]
        if not text.startswith(lit_, at):
            return None
        at += len(lit_)
        if k + 1 == len(pieces):
            return vals if at == len(text) else None
        for end in range(at + 1, len(text) + 1):
            r = go(k + 2, end, vals + [(pieces[k + 1], text[at:end])])
            if r is not None:
                return r
        return None
    return go(0, 0, [])


def part_split(texts, spec, site):
    """(sentences, {partN: [values]}) for a PART_TEMPLATES call site: the
    templates, then the sentences that fit none of them."""
    templates = spec["templates"]
    skip = re.compile(spec["skip"]) if "skip" in spec else None
    literal = lambda t: len(PART_RE.sub("", t))
    order = sorted(templates, key=literal, reverse=True)      # most literal text first
    values, dropped = {}, []
    for text in texts:
        if skip and skip.search(text):
            continue
        for tmpl in order:
            m = part_match(tmpl, text)
            if m is not None and not any("{" in v for _, v in m):
                for name, v in m:
                    lst = values.setdefault(name, [])
                    if v not in lst:
                        lst.append(v)
                break
        else:
            dropped.append(text)
    # sentences that fit no template are listed as they are
    return list(templates) + dropped, values


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

    # sentences of each call site, following the branches
    variants, limited, returns = site_variants(rows, params, cls)
    part_params = {}
    for (c, pc), spec in PART_TEMPLATES.items():
        if c == cls:
            full, _, _ = site_variants(rows, params, cls, PART_MAX_STATES, PART_MAX_VARIANTS)
            variants[pc], values = part_split(full.get(pc, []), spec, f"{cls:04X}:{pc:04X}")
            for name, vals in values.items():
                part_params[name] = vals
    for pc, texts in variants.items():
        if len(texts) >= MAX_VARIANTS and (cls, pc) not in PART_TEMPLATES:
            print(f"warning: {cls:04X}:{pc:04X} builds {len(texts)}+ sentences; "
                  f"describe it in PART_TEMPLATES", file=sys.stderr)

    # pass 2: emit flow + catalog
    flow, catalog = [], []
    evaluate(rows, events, params=params, emit=flow.append, catalog=catalog, cls=cls,
             variants=variants)

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

    # {call_OOOO}: the strings the function returns (e.g. ORLOK's drinks)
    calls = sorted({v for r in cat if r[0] != "param" for v in re.findall(r"\{(call_[0-9A-F]{4})\}", r[2])})
    for v in calls:
        lits = []
        for x in returns.get(int(v[5:], 16), []):
            # a returned parameter local: its values
            local = params.get(x[1:-1]) if x.startswith("{var") else None
            for y in sorted(local) if local else [x]:
                if y.startswith('"'):
                    y = y[1:-1]
                if "{" not in y and y not in lits:
                    lits.append(y)
        for x in lits:
            cat.append(("param", f"{cls:04X}:{v}", x, "param-value",
                        f"value of {{{v}}}: " + " | ".join(f'"{y}"' for y in lits)))
    for v, vals in part_params.items():
        for x in vals:
            cat.append(("param", f"{cls:04X}:{v}", x, "param-value",
                        f"value of {{{v}}}: one of {len(vals)} pieces"))
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
