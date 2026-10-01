"""
Divisibility and Division of Integers: single file (logic + Streamlit UI).
Run with:  streamlit run divisibility_app.py

Pick what you need from the choices:
    1. Divide one integer by another   (Division Algorithm + divisibility check)
    2. Divide a set of integers by one divisor
    3. Find all divisors of an integer
"""


# =====================================================================
# Helper (was imported from formatting.py)
# =====================================================================
def paren(n: int) -> str:
    """Wraps negative numbers in parentheses so signs never collide."""
    return f"({n})" if n < 0 else str(n)


# =====================================================================
# Divisibility and the Division Algorithm (same logic as divisibility.py)
# =====================================================================
def division_algorithm(a: int, d: int) -> tuple:
    """Returns (q, r) with a = q(d) + r and 0 <= r < |d|. Works for negative a and d."""
    r = a % abs(d)       # Python's % with a positive modulus is already in [0, |d|)
    q = (a - r) // d     # exact division
    return q, r


def division_lines(a: int, d: int) -> tuple:
    """Step-by-step lines for a divided by d. Returns (lines, q, r)."""
    q, r = division_algorithm(a, d)
    ad = abs(d)
    k = a // ad  # largest k with k|d| <= a

    lines = [
        "Division Algorithm: for integers a and d (d != 0) there are unique",
        "integers q and r such that a = q(d) + r, where 0 <= r < |d|.",
        "",
        f"a = {a}, d = {d}, |d| = {ad}",
        f"So 0 <= r < {ad}.",
        "",
        f"Find the largest multiple of {ad} that is not greater than {a}:",
        f"{paren(k)}({ad}) = {k * ad} <= {a} < {k * ad + ad} = {paren(k + 1)}({ad})",
        "",
        f"r = {a} - {paren(k)}({ad}) = {r}",
    ]

    if d > 0:
        lines.append(f"q = {k}")
    else:
        lines.append(f"d is negative, so q = -({paren(k)}) = {q}")
        lines.append(f"because {paren(k)}({ad}) = {paren(q)}({d})")

    lines += [
        "",
        f"{a} = {paren(q)}({d}) + {r}",
        "",
        "Check:",
        f"{paren(q)}({d}) + {r} = {q * d} + {r} = {q * d + r}",
        f"0 <= {r} < {ad}",
    ]
    return lines, q, r


def build_division(a: int, d: int) -> dict:
    """
    Returns a dict with:
      steps, answer,              (division algorithm)
      divis_steps, divis_answer   (does d divide a?)
    """
    lines, q, r = division_lines(a, d)

    if r == 0:
        divis_lines = [
            f"The remainder is r = 0, so {d} divides {a}.",
            f"{a} = {paren(q)}({d})",
            f"Therefore {d} | {a}  ({a} is a multiple of {d}).",
        ]
        divis_answer = f"{d} | {a}  (q = {q})"
    else:
        divis_lines = [
            f"The remainder is r = {r} != 0, so {d} does not divide {a}.",
            f"Therefore {d} does not divide {a}.",
        ]
        divis_answer = f"{d} does not divide {a}"

    return {
        "steps": "\n".join(lines),
        "answer": f"{a} = {paren(q)}({d}) + {r}   (q = {q}, r = {r})",
        "divis_steps": "\n".join(divis_lines),
        "divis_answer": divis_answer,
    }


def build_set_division(numbers: list, d: int) -> dict:
    """
    Divides every integer in `numbers` by the same divisor d.
    Returns a dict with: steps, answer, divisible, not_divisible, not_answer.
    """
    lines = [f"Divisor d = {d}, |d| = {abs(d)}, so 0 <= r < {abs(d)}", ""]
    divisible, not_divisible = [], []

    for a in numbers:
        q, r = division_algorithm(a, d)
        verdict = f"{d} | {a}" if r == 0 else f"{d} does not divide {a}"
        lines.append(f"{a} = {paren(q)}({d}) + {r}   ->  {verdict}")
        (divisible if r == 0 else not_divisible).append(a)

    joined = ", ".join(map(str, numbers))
    div_txt = ", ".join(map(str, divisible)) if divisible else "none"
    not_txt = ", ".join(map(str, not_divisible)) if not_divisible else "none"

    return {
        "steps": "\n".join(lines),
        "answer": f"Divisible by {d} in {{{joined}}}: {{{div_txt}}}",
        "divisible": divisible,
        "not_divisible": not_divisible,
        "not_answer": f"Not divisible by {d}: {{{not_txt}}}",
    }


def build_divisors(n: int) -> dict:
    """All integer divisors of n (n != 0), found by testing 1..sqrt(|n|)."""
    m = abs(n)
    lines, small, large = [], [], []
    i = 1
    while i * i <= m:
        q, r = division_algorithm(m, i)
        if r == 0:
            lines.append(f"{m} = {q}({i}) + 0  ->  {i} | {m}")
            small.append(i)
            if q != i:
                large.append(q)
        else:
            lines.append(f"{m} = {q}({i}) + {r}")
        i += 1

    positive = small + large[::-1]
    all_divs = sorted([-p for p in positive] + positive)
    return {
        "steps": "\n".join(lines),
        "answer": f"Positive divisors of {m}: {', '.join(map(str, positive))}",
        "all_answer": f"All divisors of {n}: {', '.join(map(str, all_divs))}",
    }


# =====================================================================
# Input helper
# =====================================================================
def parse_numbers(text: str) -> list:
    # Accept spaces and/or commas as separators
    return [int(piece) for piece in text.replace(",", " ").split()]


# =====================================================================
# Streamlit UI
# =====================================================================
CHOICE_ONE = "Divide one integer by another"
CHOICE_SET = "Divide a set of integers by one divisor"
CHOICE_DIVISORS = "Find all divisors of an integer"


def main():
    import streamlit as st

    st.title("Divisibility and Division of Integers")
    st.write("Division Algorithm (a = qd + r, 0 ≤ r < |d|), divisibility tests, and divisors of integers.")

    mode = st.radio("What do you want to do?", [CHOICE_ONE, CHOICE_SET, CHOICE_DIVISORS])
    st.divider()

    # ---------------- 1. One integer divided by another ----------------
    if mode == CHOICE_ONE:
        col1, col2 = st.columns(2)
        a_text = col1.text_input("Dividend (a)", placeholder="e.g. -17", key="one_a")
        d_text = col2.text_input("Divisor (d)", placeholder="e.g. 5", key="one_d")

        if st.button("Calculate", key="one_btn"):
            try:
                a, d = int(a_text), int(d_text)
            except ValueError:
                st.error("Invalid input. Enter whole numbers only.")
                st.stop()
            if d == 0:
                st.error("The divisor cannot be zero.")
                st.stop()

            res = build_division(a, d)

            st.subheader("Final Answers")
            st.success(res["answer"])
            st.success(res["divis_answer"])

            st.divider()
            st.subheader("Division Algorithm Solution")
            st.code(res["steps"], language="text")

            st.divider()
            st.subheader("Divisibility")
            st.code(res["divis_steps"], language="text")
            st.info(res["divis_answer"])

    # ---------------- 2. A set divided by one divisor ----------------
    elif mode == CHOICE_SET:
        set_text = st.text_input(
            "Set of integers (separated by spaces or commas)",
            placeholder="e.g. 12 -17 25 40 7",
            key="set_nums",
        )
        d_text = st.text_input("Divisor (d)", placeholder="e.g. 5", key="set_d")

        if st.button("Calculate", key="set_btn"):
            try:
                nums = parse_numbers(set_text)
                d = int(d_text)
            except ValueError:
                st.error("Invalid input. Enter whole numbers only.")
                st.stop()
            if not nums:
                st.error("Enter at least one integer.")
                st.stop()
            if d == 0:
                st.error("The divisor cannot be zero.")
                st.stop()

            res = build_set_division(nums, d)

            st.subheader("Final Answers")
            st.success(res["answer"])
            st.success(res["not_answer"])

            st.divider()
            st.subheader("Solution")
            st.code(res["steps"], language="text")

    # ---------------- 3. All divisors of an integer ----------------
    else:
        n_text = st.text_input("Integer (n)", placeholder="e.g. 36", key="divisors_n")

        if st.button("Calculate", key="divisors_btn"):
            try:
                n = int(n_text)
            except ValueError:
                st.error("Invalid input. Enter a whole number.")
                st.stop()
            if n == 0:
                st.error("Every nonzero integer divides 0, so please enter a nonzero integer.")
                st.stop()

            res = build_divisors(n)

            st.subheader("Final Answers")
            st.success(res["answer"])
            st.success(res["all_answer"])

            st.divider()
            st.subheader("Solution (testing each i up to √|n|)")
            st.code(res["steps"], language="text")


if __name__ == "__main__":
    main()
