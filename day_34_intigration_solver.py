# integration_solver_app.py

import streamlit as st
import sympy as sp
from sympy.integrals.manualintegrate import integral_steps
import mpmath as mp

# -----------------------------
# Utility Functions
# -----------------------------

def symbolic_integration(expr_str, var_str):
    x = sp.symbols(var_str)
    expr = sp.sympify(expr_str)

    # Indefinite integral
    result = sp.integrate(expr, x)

    # Step extraction
    try:
        steps = integral_steps(expr, x)
    except Exception as e:
        steps = f"Step extraction failed: {e}"

    return result, steps


def definite_integration(expr_str, var_str, a, b):
    x = sp.symbols(var_str)
    expr = sp.sympify(expr_str)

    symbolic = sp.integrate(expr, (x, a, b))

    return symbolic


def numerical_verify(expr_str, antiderivative, a, b, precision=50):
    mp.mp.dps = precision
    x = sp.symbols('x')

    f_expr = sp.sympify(expr_str)
    F_expr = sp.sympify(antiderivative)

    f = sp.lambdify(x, f_expr, 'mpmath')
    F = sp.lambdify(x, F_expr, 'mpmath')

    try:
        num_val = mp.quad(f, [a, b], method='tanh-sinh')
        sym_val = F(b) - F(a)
        return mp.almosteq(num_val, sym_val), num_val, sym_val
    except Exception as e:
        return False, None, str(e)


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Neuro-Symbolic Integration Solver", layout="centered")

st.title("🧠 Neuro-Symbolic Integration Solver")
st.write("Definite & Indefinite Integration with Step-by-Step Logic")

expr_input = st.text_input(
    "Enter integrand (example: x*exp(x) or sin(x)/x):",
    value="x*exp(x)"
)

var = st.text_input("Variable of integration:", value="x")

mode = st.radio("Select Mode:", ["Indefinite", "Definite"])

if mode == "Definite":
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Lower limit (a):", value=0.0)
    with col2:
        b = st.number_input("Upper limit (b):", value=1.0)

st.divider()

if st.button("Solve Integration 🚀"):
    try:
        x = sp.symbols(var)
        st.subheader("📘 Problem")
        st.latex(r"\int " + sp.latex(sp.sympify(expr_input)) + r"\, d" + var)

        if mode == "Indefinite":
            result, steps = symbolic_integration(expr_input, var)

            st.subheader("✅ Symbolic Result")
            st.latex(sp.latex(result) + " + C")

            st.subheader("🧩 Step-by-Step Logic")
            st.code(str(steps), language="text")

        else:
            sym_def = definite_integration(expr_input, var, a, b)

            st.subheader("✅ Symbolic Definite Result")
            st.latex(sp.latex(sym_def))

            # Numerical verification
            ok, num_val, sym_val = numerical_verify(
                expr_input,
                sp.integrate(sp.sympify(expr_input), x),
                a, b
            )

            st.subheader("🔍 Numerical Verification (Tanh-Sinh)")
            if ok:
                st.success("✔ Symbolic result VERIFIED numerically")
            else:
                st.warning("⚠ Verification failed or approximate")

            if num_val is not None:
                st.write("Numerical Integral:", num_val)
                st.write("Symbolic F(b) − F(a):", sym_val)

    except Exception as e:
        st.error(f"Error: {e}")
