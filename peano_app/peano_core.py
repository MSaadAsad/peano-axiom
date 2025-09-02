from __future__ import annotations


class PeanoAxioms:
    """Implements Peano Arithmetic (PA) with tracing and step counting.
    
    Peano axioms:
      - A1: 0 is a natural number
      - A2: If x is natural, s(x) is natural  
      - A3: s(x) ≠ 0 for all x
      - A4: s(x) = s(y) → x = y (injectivity)
      - A5: Induction schema (implicit in recursive definitions)
      
    Primitive recursive definitions (derived from axioms):
      - add(x, 0) = x; add(x, s(y)) = s(add(x, y))
      - mult(x, 0) = 0; mult(x, s(y)) = mult(x, y) + x
      
    Other derived operations:
      - predecessor, subtraction (clamped), division, modulo, gcd
    """

    def __init__(self) -> None:
        self.steps: int = 0
        self.negative_encountered: bool = False
        self.trace_stack: list[dict] = []
        self.trace_root: dict | None = None

    # ----- Basic term utilities -----
    @staticmethod
    def normalize(term: str) -> str:
        return term.replace(" ", "")

    def _step(self) -> None:
        self.steps += 1

    # ----- Tracing helpers -----
    def start_trace(self) -> None:
        self.steps = 0
        self.negative_encountered = False
        self.trace_stack = []
        self.trace_root = None

    def _enter(self, op: str, args: list[str]) -> dict:
        node = {"op": op, "args": args[:], "children": [], "result": None, "axiom": None}
        if not self.trace_stack:
            self.trace_root = node
        else:
            self.trace_stack[-1]["children"].append(node)
        self.trace_stack.append(node)
        return node

    def _exit(self, node: dict, result: str | bool) -> None:
        node["result"] = result
        if self.trace_stack and self.trace_stack[-1] is node:
            self.trace_stack.pop()

    def get_trace_flat(self) -> list[dict]:
        out: list[dict] = []

        def walk(n: dict, depth: int) -> None:
            out.append({
                "depth": depth,
                "op": n["op"],
                "args": n["args"],
                "result": n["result"],
                "axiom": n.get("axiom"),
            })
            for c in n.get("children", []):
                walk(c, depth + 1)

        if self.trace_root is not None:
            walk(self.trace_root, 0)
        return out

    def is_zero(self, x: str) -> bool:
        self._step()
        node = self._enter("is_zero", [x])
        s = self.normalize(x)
        if s == "0":
            node["axiom"] = "A1"  # 0 is a natural number
            self._exit(node, True)
            return True
        else:
            self._exit(node, False)
            return False

    def successor(self, x: str) -> str:
        self._step()
        node = self._enter("successor", [x])
        res = f"s({self.normalize(x)})"
        self._exit(node, res)
        return res

    def predecessor(self, x: str) -> str:
        self._step()
        node = self._enter("predecessor", [x])
        s = self.normalize(x)
        if s == "0":
            res = "0"
            self._exit(node, res)
            return res
        if not s.startswith("s(") or not s.endswith(")"):
            self._exit(node, "error")
            raise ValueError(f"Invalid Peano representation: {x}")
        res = s[2:-1]
        self._exit(node, res)
        return res

    # ----- Axioms A1, A2 -----
    def peano(self, x: str) -> bool:
        self._step()
        node = self._enter("peano", [x])
        s = self.normalize(x)
        if s == "0":
            node["axiom"] = "A1"
            self._exit(node, True)
            return True
        if s.startswith("s(") and s.endswith(")"):
            node["axiom"] = "A2"
            res = self.peano(self.predecessor(s))
            self._exit(node, res)
            return res
        self._exit(node, False)
        return False

    # ----- Equality using A3, A4 -----
    def equal(self, x: str, y: str) -> bool:
        self._step()
        node = self._enter("equal", [x, y])
        xs, ys = self.normalize(x), self.normalize(y)
        if xs == "0" and ys == "0":
            self._exit(node, True)
            return True
        if xs == "0" or ys == "0":  # A3
            node["axiom"] = "A3"
            self._exit(node, False)
            return False
        node["axiom"] = "A4"
        res = self.equal(self.predecessor(xs), self.predecessor(ys))
        self._exit(node, res)
        return res

    def greater_than(self, x: str, y: str) -> bool:
        self._step()
        node = self._enter("greater_than", [x, y])
        res = (not self.equal(x, y)) and (not self.less_than(x, y))
        self._exit(node, res)
        return res

    # ----- Definitional extensions -----
    def add(self, x: str, y: str) -> str:
        """Addition by primitive recursion: add(x,0)=x; add(x,s(y))=s(add(x,y))."""
        self._step()
        node = self._enter("add", [x, y])
        ys = self.normalize(y)
        if ys == "0":
            node["definition"] = "ADD-BASE"  # add(x,0) = x
            res = self.normalize(x)
            self._exit(node, res)
            return res
        if not ys.startswith("s("):
            self._exit(node, "error")
            raise ValueError(f"Invalid Peano representation: {y}")
        node["definition"] = "ADD-REC"  # add(x,s(y)) = s(add(x,y))
        # The result is s(add(x, pred(y))) but we don't compute it separately
        # We show the equation directly as the definition requires
        inner_y = self.predecessor(ys)
        inner_result = self.add(x, inner_y)
        res = f"s({inner_result})"
        self._exit(node, res)
        return res

    def multiply(self, x: str, y: str) -> str:
        """Multiplication by primitive recursion: mult(x,0)=0; mult(x,s(y))=mult(x,y)+x."""
        self._step()
        node = self._enter("multiply", [x, y])
        ys = self.normalize(y)
        if ys == "0":
            node["definition"] = "MULT-BASE"  # mult(x,0) = 0
            res = "0"
            self._exit(node, res)
            return res
        if not ys.startswith("s("):
            self._exit(node, "error")
            raise ValueError(f"Invalid Peano representation: {y}")
        node["definition"] = "MULT-REC"  # mult(x,s(y)) = mult(x,y) + x
        # Show the recursive step explicitly
        inner_y = self.predecessor(ys)
        mult_result = self.multiply(x, inner_y)
        res = self.add(mult_result, x)
        self._exit(node, res)
        return res

    def less_than(self, x: str, y: str) -> bool:
        self._step()
        node = self._enter("less_than", [x, y])
        xs, ys = self.normalize(x), self.normalize(y)
        if xs == "0" and ys == "0":
            node["definition"] = "LT-BASE"  # lt(0,0) = false
            self._exit(node, False)
            return False
        if xs == "0" and ys != "0":
            node["definition"] = "LT-BASE"  # lt(0,s(x)) = true
            self._exit(node, True)
            return True
        if xs != "0" and ys == "0":
            node["definition"] = "LT-BASE"  # lt(s(x),0) = false
            self._exit(node, False)
            return False
        node["definition"] = "LT-REC"  # lt(s(x),s(y)) = lt(x,y)
        res = self.less_than(self.predecessor(xs), self.predecessor(ys))
        self._exit(node, res)
        return res

    def subtract(self, x: str, y: str) -> str:
        self._step()
        node = self._enter("subtract", [x, y])
        xs, ys = self.normalize(x), self.normalize(y)
        if ys == "0":
            node["definition"] = "SUB-BASE"  # sub(x,0) = x
            self._exit(node, xs)
            return xs
        if xs == "0":
            node["definition"] = "SUB-BASE"  # sub(0,s(y)) = 0 (clamped)
            self.negative_encountered = True
            self._exit(node, "0")
            return "0"
        node["definition"] = "SUB-REC"  # sub(s(x),s(y)) = sub(x,y)
        res = self.subtract(self.predecessor(xs), self.predecessor(ys))
        self._exit(node, res)
        return res

    # Division and modulo via repeated subtraction (not primitive Peano, but definitional extension)
    def div_peano(self, x: str, y: str) -> str:
        self._step()
        node = self._enter("div", [x, y])
        node["definition"] = "DIV-DEF"  # div(x,y) = repeated subtraction
        ys = self.normalize(y)
        if ys == "0":
            self._exit(node, "error")
            raise ValueError("division by zero")

        def helper(rem: str, den: str, acc: str) -> str:
            self._step()
            hnode = self._enter("div_step", [rem, den, acc])
            hnode["definition"] = "DIV-STEP"
            res = acc if self.less_than(rem, den) else helper(self.subtract(rem, den), den, self.successor(acc))
            self._exit(hnode, res)
            return res

        res = helper(self.normalize(x), ys, "0")
        self._exit(node, res)
        return res

    def mod_peano(self, x: str, y: str) -> str:
        self._step()
        node = self._enter("mod", [x, y])
        node["definition"] = "MOD-DEF"  # mod(x,y) = remainder after repeated subtraction
        ys = self.normalize(y)
        if ys == "0":
            self._exit(node, "error")
            raise ValueError("modulo by zero")

        def helper(rem: str, den: str) -> str:
            self._step()
            hnode = self._enter("mod_step", [rem, den])
            hnode["definition"] = "MOD-STEP"
            res = rem if self.less_than(rem, den) else helper(self.subtract(rem, den), den)
            self._exit(hnode, res)
            return res

        res = helper(self.normalize(x), ys)
        self._exit(node, res)
        return res

    def gcd_peano(self, x: str, y: str) -> str:
        self._step()
        node = self._enter("gcd", [x, y])
        ys = self.normalize(y)
        if ys == "0":
            node["definition"] = "GCD-BASE"  # gcd(x,0) = x
            res = self.normalize(x)
            self._exit(node, res)
            return res
        node["definition"] = "GCD-REC"  # gcd(x,y) = gcd(y, mod(x,y))
        res = self.gcd_peano(ys, self.mod_peano(x, ys))
        self._exit(node, res)
        return res

