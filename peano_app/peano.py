from __future__ import annotations
from dataclasses import dataclass
from peano_app.peano_core import PeanoAxioms


def int_to_peano_str(n: int) -> str:
    if n < 0:
        raise ValueError("Peano naturals are non-negative")
    if n == 0:
        return "0"
    return f"s({int_to_peano_str(n - 1)})"


def peano_str_to_int(peano: str) -> int:
    # Robust to whitespace
    s = peano.replace(" ", "")
    if s == "0":
        return 0
    # Count occurrences of 's(' assuming canonical nesting
    if not s.startswith("s(") or not s.endswith(")"):
        raise ValueError(f"Invalid Peano representation: {peano}")
    return s.count("s(")


AXIOMS = PeanoAxioms()


def is_zero(peano: str) -> bool:
    return AXIOMS.is_zero(peano)


def successor(peano: str) -> str:
    return AXIOMS.successor(peano)


def predecessor(peano: str) -> str:
    return AXIOMS.predecessor(peano)


def add(x: str, y: str) -> str:
    return AXIOMS.add(x, y)


def multiply(x: str, y: str) -> str:
    return AXIOMS.multiply(x, y)


def less_than(x: str, y: str) -> bool:
    return AXIOMS.less_than(x, y)


def subtract(x: str, y: str) -> str:
    return AXIOMS.subtract(x, y)


def to_display(peano: str) -> dict:
    return {
        "peano": peano,
        "int": peano_str_to_int(peano),
    }


# Additional comparisons
def equal(x: str, y: str) -> bool:
    return AXIOMS.equal(x, y)


def greater_than(x: str, y: str) -> bool:
    return AXIOMS.greater_than(x, y)


# Division and modulo via repeated subtraction
def div_peano(x: str, y: str) -> str:
    return AXIOMS.div_peano(x, y)


def mod_peano(x: str, y: str) -> str:
    return AXIOMS.mod_peano(x, y)


def gcd_peano(x: str, y: str) -> str:
    return AXIOMS.gcd_peano(x, y)


@dataclass(frozen=True)
class PeanoFraction:
    numerator: str
    denominator: str


def make_fraction(numerator: str, denominator: str) -> PeanoFraction:
    if denominator.replace(" ", "") == "0":
        raise ValueError("denominator cannot be 0")
    return PeanoFraction(numerator.replace(" ", ""), denominator.replace(" ", ""))


def peano_to_fraction(x: str) -> PeanoFraction:
    return PeanoFraction(x.replace(" ", ""), successor("0"))


def simplify_fraction(frac: PeanoFraction) -> PeanoFraction:
    g = gcd_peano(frac.numerator, frac.denominator)
    return PeanoFraction(div_peano(frac.numerator, g), div_peano(frac.denominator, g))


def to_display_fraction(frac: PeanoFraction) -> dict:
    return {
        "numerator": to_display(frac.numerator),
        "denominator": to_display(frac.denominator),
    }


# Fraction arithmetic (pure Peano naturals; subtraction clamps at 0)
def add_fractions(a: PeanoFraction, b: PeanoFraction) -> PeanoFraction:
    num = add(multiply(a.numerator, b.denominator), multiply(b.numerator, a.denominator))
    den = multiply(a.denominator, b.denominator)
    return simplify_fraction(PeanoFraction(num, den))


def subtract_fractions(a: PeanoFraction, b: PeanoFraction) -> PeanoFraction:
    num = subtract(multiply(a.numerator, b.denominator), multiply(b.numerator, a.denominator))
    den = multiply(a.denominator, b.denominator)
    return simplify_fraction(PeanoFraction(num, den))


def multiply_fractions(a: PeanoFraction, b: PeanoFraction) -> PeanoFraction:
    num = multiply(a.numerator, b.numerator)
    den = multiply(a.denominator, b.denominator)
    return simplify_fraction(PeanoFraction(num, den))


def divide_fractions(a: PeanoFraction, b: PeanoFraction) -> PeanoFraction:
    if equal(b.numerator, "0"):
        raise ValueError("division by zero in fraction")
    num = multiply(a.numerator, b.denominator)
    den = multiply(a.denominator, b.numerator)
    return simplify_fraction(PeanoFraction(num, den))


def describe_fraction(numerator: str, denominator: str) -> dict:
    """Return rich info about a fraction n/d using Peano operations.

    Includes gcd, simplified fraction, and the division relation
    n = d*q + r with both int and Peano renderings.
    """
    num = numerator.replace(" ", "")
    den = denominator.replace(" ", "")
    if den == "0":
        raise ValueError("denominator cannot be 0")

    g = gcd_peano(num, den)
    simp = PeanoFraction(div_peano(num, g), div_peano(den, g))

    q = div_peano(num, den)
    r = mod_peano(num, den)
    product = multiply(den, q)
    rhs = add(product, r)

    return {
        "numerator": to_display(num),
        "denominator": to_display(den),
        "gcd": to_display(g),
        "simplified": {
            "numerator": to_display(simp.numerator),
            "denominator": to_display(simp.denominator),
        },
        "division": {
            "quotient": to_display(q),
            "remainder": to_display(r),
            "check": {
                "lhs": to_display(num),
                "product": to_display(product),
                "rhs": to_display(rhs),
            },
        },
    }


def reset_step_counter() -> None:
    AXIOMS.steps = 0


def get_step_count() -> int:
    return AXIOMS.steps


def start_trace() -> None:
    AXIOMS.start_trace()


def get_trace_flat() -> list[dict]:
    return AXIOMS.get_trace_flat()


def get_negative_flag() -> bool:
    return AXIOMS.negative_encountered


# ---------- Trace interpretation helpers ----------
def _is_peano_term(val: object) -> bool:
    return isinstance(val, str) and (val == "0" or (val.startswith("s(") and val.endswith(")")))


def _to_int_if_peano(val: object) -> object:
    if _is_peano_term(val):
        return peano_str_to_int(val)  # may raise if malformed
    return val


def _to_int_maybe(val: object) -> object:
    try:
        return _to_int_if_peano(val)
    except Exception:
        return None


def _fmt_int_expr(op: str, args: list[object], result: object) -> str:
    # Attempt to convert args/results to ints and build a compact meaning
    try:
        iargs = [_to_int_if_peano(a) for a in args]
        ires = _to_int_if_peano(result)
    except Exception:
        return ""

    def as_str(x: object) -> str:
        return str(x)

    if op == "successor" and len(iargs) == 1 and isinstance(ires, int):
        return f"{as_str(iargs[0])} + 1 = {ires}"
    if op == "predecessor" and len(iargs) == 1 and isinstance(ires, (int, str)):
        try:
            n = int(iargs[0])
            m = int(ires) if isinstance(ires, int) else None
        except Exception:
            n, m = None, None
        if n is not None and m is not None:
            suffix = " (clamped)" if n == 0 and m == 0 else ""
            return f"{n} - 1 = {m}{suffix}"
        return ""
    if op == "add" and len(iargs) == 2 and isinstance(ires, int):
        return f"{as_str(iargs[0])} + {as_str(iargs[1])} = {ires}"
    if op == "subtract" and len(iargs) == 2 and isinstance(ires, (int, str)):
        try:
            a = int(iargs[0])
            b = int(iargs[1])
            c = int(ires) if isinstance(ires, int) else None
        except Exception:
            a = b = c = None
        if a is not None and b is not None and c is not None:
            suffix = " (clamped)" if a < b and c == 0 else ""
            return f"{a} - {b} = {c}{suffix}"
        return ""
    if op == "multiply" and len(iargs) == 2 and isinstance(ires, int):
        return f"{as_str(iargs[0])} × {as_str(iargs[1])} = {ires}"
    if op in ("less_than", "equal", "greater_than") and len(iargs) == 2 and isinstance(ires, bool):
        symbol = {"less_than": "<", "equal": "=", "greater_than": ">"}[op]
        return f"{as_str(iargs[0])} {symbol} {as_str(iargs[1])} = {ires}"
    if op == "div" and len(iargs) == 2 and isinstance(ires, int):
        return f"{as_str(iargs[0])} ÷ {as_str(iargs[1])} = {ires}"
    if op == "mod" and len(iargs) == 2 and (_is_peano_term(result) or isinstance(ires, int)):
        return f"{as_str(iargs[0])} mod {as_str(iargs[1])} = {as_str(ires)}"
    if op == "gcd" and len(iargs) == 2 and (_is_peano_term(result) or isinstance(ires, int)):
        return f"gcd({as_str(iargs[0])}, {as_str(iargs[1])}) = {as_str(ires)}"
    if op in ("div_step", "mod_step") and len(iargs) >= 2:
        return "step"
    if op in ("is_zero", "peano"):
        return "predicate"
    return ""


def _fmt_peano_expr(op: str, args: list[object], result: object) -> str:
    try:
        pargs = [a for a in args]
        pres = result
    except Exception:
        return ""

    def as_str(x: object) -> str:
        return str(x)

    if op == "successor" and len(pargs) == 1:
        return f"successor: {as_str(pargs[0])} → {as_str(pres)}"
    if op == "predecessor" and len(pargs) == 1:
        return f"pred (derived): {as_str(pargs[0])} → {as_str(pres)}"
    if op == "add" and len(pargs) == 2:
        return f"add: {as_str(pargs[0])} + {as_str(pargs[1])} → {as_str(pres)}"
    if op == "subtract" and len(pargs) == 2:
        return f"sub (derived, clamped): {as_str(pargs[0])} − {as_str(pargs[1])} → {as_str(pres)}"
    if op == "multiply" and len(pargs) == 2:
        return f"mult: {as_str(pargs[0])} × {as_str(pargs[1])} → {as_str(pres)}"
    if op in ("less_than", "equal", "greater_than") and len(pargs) == 2:
        symbol = {"less_than": "<", "equal": "=", "greater_than": ">"}[op]
        return f"compare: {as_str(pargs[0])} {symbol} {as_str(pargs[1])} → {as_str(result)}"
    if op == "div" and len(pargs) == 2:
        return f"divide: {as_str(pargs[0])} ÷ {as_str(pargs[1])} → {as_str(pres)}"
    if op == "mod" and len(pargs) == 2:
        return f"mod: {as_str(pargs[0])} mod {as_str(pargs[1])} → {as_str(pres)}"
    if op == "gcd" and len(pargs) == 2:
        return f"gcd: {as_str(pargs[0])}, {as_str(pargs[1])} → {as_str(pres)}"
    if op in ("div_step", "mod_step") and len(pargs) >= 2:
        return "step"
    if op in ("is_zero", "peano"):
        return "predicate"
    return ""


def get_trace_enriched() -> list[dict]:
    raw = get_trace_flat()
    enriched: list[dict] = []
    for n in raw:
        op = n.get("op")
        args = n.get("args", [])
        res = n.get("result")
        meaning_int = _fmt_int_expr(op, args, res)
        meaning_peano = _fmt_peano_expr(op, args, res)
        explanation = _explain_nl(op, args, res, n.get("axiom"))
        axiom = n.get("axiom")
        args_int = [_to_int_maybe(a) for a in args]
        result_int = _to_int_maybe(res)
        enriched.append({
            **n,
            "meaning": meaning_int,
            "meaning_peano": meaning_peano,
            "explanation": explanation,
            "axiom": axiom,
            "definition": n.get("definition"),
            "args_int": args_int,
            "result_int": result_int,
        })
    return enriched


def _explain_nl(op: str, args: list[object], result: object, axiom: object) -> str:
    a = [str(x) for x in args]
    r = str(result)
    if op == "successor":
        return f"Successor of {a[0]} is {r}."
    if op == "predecessor":
        return f"Predecessor of {a[0]} (clamped at 0) is {r}."
    if op == "add":
        return f"Add {a[0]} and {a[1]} → {r}."
    if op == "subtract":
        return f"Subtract {a[1]} from {a[0]} (clamped at 0) → {r}."
    if op == "multiply":
        return f"Multiply {a[0]} by {a[1]} (repeated addition) → {r}."
    if op == "less_than":
        return f"Check {a[0]} < {a[1]} → {r}."
    if op == "equal":
        return f"Check {a[0]} = {a[1]} → {r}."
    if op == "greater_than":
        return f"Check {a[0]} > {a[1]} → {r}."
    if op == "div":
        return f"Divide {a[0]} by {a[1]} (repeated subtraction) → quotient {r}."
    if op == "mod":
        return f"Compute {a[0]} mod {a[1]} (repeated subtraction) → remainder {r}."
    if op == "gcd":
        return f"gcd({a[0]}, {a[1]}) via Euclidean method → {r}."
    if op == "div_step":
        return "Division step: if remainder < divisor stop; otherwise subtract divisor and increment quotient."
    if op == "mod_step":
        return "Modulo step: if remainder < divisor stop; otherwise subtract divisor and continue."
    if op in ("peano", "is_zero"):
        return "Predicate evaluation."
    return ""

