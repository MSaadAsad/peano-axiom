from __future__ import annotations

from flask import Flask, render_template, request

from peano_app.peano import (
    int_to_peano_str,
    successor,
    predecessor,
    add,
    multiply,
    less_than,
    subtract,
    to_display,
    equal,
    greater_than,
    div_peano,
    mod_peano,
    gcd_peano,
    make_fraction,
    peano_to_fraction,
    simplify_fraction,
    to_display_fraction,
    get_step_count,
    start_trace,
    get_negative_flag,
    get_trace_enriched,
    add_fractions,
    subtract_fractions,
    multiply_fractions,
    divide_fractions,
)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        result = None
        error = None

        # Defaults for the form
        op = request.form.get("operation", "successor")
        input_mode = request.form.get("input_mode", "natural")
        x_raw = request.form.get("x", "2")
        y_raw = request.form.get("y", "3")
        x_num_raw = request.form.get("x_num", "1")
        x_den_raw = request.form.get("x_den", "1")
        y_num_raw = request.form.get("y_num", "1")
        y_den_raw = request.form.get("y_den", "1")

        try:
            x_val = max(0, int(x_raw))
            y_val = max(0, int(y_raw))

            x_peano = int_to_peano_str(x_val)
            y_peano = int_to_peano_str(y_val)

            # Fractions (if selected)
            x_num_val = max(0, int(x_num_raw))
            x_den_val = max(1, int(x_den_raw))
            y_num_val = max(0, int(y_num_raw))
            y_den_val = max(1, int(y_den_raw))

            x_frac = make_fraction(int_to_peano_str(x_num_val), int_to_peano_str(x_den_val))
            y_frac = make_fraction(int_to_peano_str(y_num_val), int_to_peano_str(y_den_val))

            # Normalize operation to match input mode
            natural_ops = {
                "successor",
                "predecessor",
                "add",
                "subtract",
                "multiply",
                "less_than",
                "equal",
                "greater_than",
                "div",
                "mod",
                "gcd",
                "to_fraction",
                "simplify_fraction",
            }
            fraction_ops = {
                "simplify_fraction_input",
                "add_fractions",
                "subtract_fractions",
                "multiply_fractions",
                "divide_fractions",
            }
            if input_mode == "fraction" and op not in fraction_ops:
                op = "multiply_fractions"
            if input_mode == "natural" and op not in natural_ops:
                op = "multiply"

            if request.method == "POST":
                start_trace()
                if op == "successor":
                    res_peano = successor(x_peano)
                    result = {
                        "operation": "successor",
                        "x": to_display(x_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "predecessor":
                    res_peano = predecessor(x_peano)
                    result = {
                        "operation": "predecessor",
                        "x": to_display(x_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "add":
                    res_peano = add(x_peano, y_peano)
                    result = {
                        "operation": "add",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "multiply":
                    res_peano = multiply(x_peano, y_peano)
                    result = {
                        "operation": "multiply",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "subtract":
                    res_peano = subtract(x_peano, y_peano)
                    result = {
                        "operation": "subtract (clamped at 0)",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "less_than":
                    lt = less_than(x_peano, y_peano)
                    result = {
                        "operation": "less than",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": {"peano": str(lt), "int": lt},
                    }
                elif op == "equal":
                    eq = equal(x_peano, y_peano)
                    result = {
                        "operation": "equal",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": {"peano": str(eq), "int": eq},
                    }
                elif op == "greater_than":
                    gt = greater_than(x_peano, y_peano)
                    result = {
                        "operation": "greater than",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": {"peano": str(gt), "int": gt},
                    }
                elif op == "div":
                    res_peano = div_peano(x_peano, y_peano)
                    result = {
                        "operation": "div",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "mod":
                    res_peano = mod_peano(x_peano, y_peano)
                    result = {
                        "operation": "mod",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "gcd":
                    res_peano = gcd_peano(x_peano, y_peano)
                    result = {
                        "operation": "gcd",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": to_display(res_peano),
                    }
                elif op == "to_fraction":
                    frac = peano_to_fraction(x_peano)
                    result = {
                        "operation": "to fraction (X/1)",
                        "x": to_display(x_peano),
                        "result": to_display_fraction(frac),
                    }
                elif op == "simplify_fraction":
                    frac = make_fraction(x_peano, y_peano)
                    sfrac = simplify_fraction(frac)
                    result = {
                        "operation": "simplify ratio (X/Y)",
                        "x": to_display(x_peano),
                        "y": to_display(y_peano),
                        "result": to_display_fraction(sfrac),
                    }
                elif op == "simplify_fraction_input":
                    sfrac = simplify_fraction(x_frac)
                    result = {
                        "operation": "simplify",
                        "x_frac": to_display_fraction(x_frac),
                        "result": to_display_fraction(sfrac),
                    }
                elif op == "add_fractions":
                    res = add_fractions(x_frac, y_frac)
                    result = {
                        "operation": "add",
                        "x_frac": to_display_fraction(x_frac),
                        "y_frac": to_display_fraction(y_frac),
                        "result": to_display_fraction(res),
                    }
                elif op == "subtract_fractions":
                    res = subtract_fractions(x_frac, y_frac)
                    result = {
                        "operation": "subtract",
                        "x_frac": to_display_fraction(x_frac),
                        "y_frac": to_display_fraction(y_frac),
                        "result": to_display_fraction(res),
                    }
                elif op == "multiply_fractions":
                    res = multiply_fractions(x_frac, y_frac)
                    result = {
                        "operation": "multiply",
                        "x_frac": to_display_fraction(x_frac),
                        "y_frac": to_display_fraction(y_frac),
                        "result": to_display_fraction(res),
                    }
                elif op == "divide_fractions":
                    res = divide_fractions(x_frac, y_frac)
                    result = {
                        "operation": "divide",
                        "x_frac": to_display_fraction(x_frac),
                        "y_frac": to_display_fraction(y_frac),
                        "result": to_display_fraction(res),
                    }
                else:
                    error = "Unsupported operation"

            # Build filtered trace (limit depth to 10)
            full_trace = get_trace_enriched()
            max_depth_val = 10

            # Filter trace by depth and hide clutter
            filtered_trace = []
            for n in full_trace:
                if n.get("depth", 0) > max_depth_val:
                    continue
                
                # Hide operations that clutter the formal derivation
                op = n.get("op", "")
                if op in ("predecessor", "successor"):
                    # These are implementation details, not part of the formal derivation
                    continue
                    
                filtered_trace.append(n)

            return render_template(
                "index.html",
                operation=op,
                input_mode=input_mode,
                x=x_raw,
                y=y_raw,
                x_num=x_num_raw,
                x_den=x_den_raw,
                y_num=y_num_raw,
                y_den=y_den_raw,
                result=result,
                error=error,
                steps=get_step_count(),
                trace=filtered_trace,
                negative=get_negative_flag(),
            )
        except Exception as exc:  # minimal logs per user preference
            error = str(exc)
            return render_template(
                "index.html",
                operation=op,
                x=x_raw,
                y=y_raw,
                result=result,
                error=error,
            )

    return app


app = create_app()

