"""
Divisibility and Division of Integers: single file (logic + Streamlit UI).
Run with:  streamlit run divisibility_app.py

One search bar. Type any of these:
    -17 / 5                  Division Algorithm: -17 = q(5) + r
    12 -17 25 40 / 5         Divide a set of integers by 5
    5 | 20                   Does 5 divide 20?
    5 | 10 20 33 -45         Does 5 divide each number in the set?
    divisors 36              All divisors of 36
Numbers may be separated by spaces and/or commas.
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
# Search-bar parsing
# =====================================================================
def parse_numbers(text: str) -> list:
    # Accept spaces and/or commas as separators
    return [int(piece) for piece in text.replace(",", " ").split()]


def parse_query(query: str) -> tuple:
    """
    Reads the search bar text. Returns one of:
      ("divisors", n)
      ("divide", numbers, d)      numbers has one or more integers
    Raises ValueError with a friendly message on bad input.
    """
    text = query.strip().replace("÷", "/")
    if not text:
        raise ValueError("Type something in the search bar first.")

    # divisors 36
    if text.lower().startswith("divisors"):
        try:
            nums = parse_numbers(text[len("divisors"):])
        except ValueError:
            raise ValueError("Use whole numbers only, e.g. divisors 36")
        if len(nums) != 1 or nums[0] == 0:
            raise ValueError("Use: divisors n   (one nonzero integer), e.g. divisors 36")
        return ("divisors", nums[0])

    # 5 | 10 20 33     (d divides each number)
    if "|" in text:
        left, right = text.split("|", 1)
        try:
            ds, nums = parse_numbers(left), parse_numbers(right)
        except ValueError:
            raise ValueError("Use whole numbers only, e.g. 5 | 20")
        if len(ds) != 1 or not nums:
            raise ValueError("Use: d | a   or   d | a b c ...   e.g. 5 | 10 20 33")
        d = ds[0]

    # -17 / 5   or   12 -17 25 40 / 5
    elif "/" in text:
        left, right = text.rsplit("/", 1)
        try:
            nums, ds = parse_numbers(left), parse_numbers(right)
        except ValueError:
            raise ValueError("Use whole numbers only, e.g. -17 / 5")
        if len(ds) != 1 or not nums:
            raise ValueError("Use: a / d   or   a b c ... / d   e.g. 12 -17 25 / 5")
        d = ds[0]

    else:
        raise ValueError("Use  a / d,  a b c / d,  d | a,  or  divisors n.")

    if d == 0:
        raise ValueError("The divisor cannot be zero.")
    return ("divide", nums, d)


# =====================================================================
# Streamlit UI
# =====================================================================
def main():
    import streamlit as st

    st.title("Divisibility and Division of Integers")
    st.write("Division Algorithm (a = qd + r, 0 ≤ r < |d|), divisibility tests, and divisors of integers.")

    query = st.text_input(
        "Search bar",
        placeholder="e.g.  -17 / 5   |   12 -17 25 40 / 5   |   5 | 20   |   divisors 36",
    )
    st.caption(
        "a / d: divide.  a b c / d: divide a set.  d | a: does d divide a?  divisors n: list divisors."
    )

    if st.button("Calculate"):
        try:
            parsed = parse_query(query)
        except ValueError as err:
            st.error(str(err))
            st.stop()

        if parsed[0] == "divisors":
            res = build_divisors(parsed[1])

            st.subheader("Final Answers")
            st.success(res["answer"])
            st.success(res["all_answer"])

            st.divider()
            st.subheader("Solution (testing each i up to √|n|)")
            st.code(res["steps"], language="text")

        else:
            _, nums, d = parsed

            if len(nums) == 1:
                res = build_division(nums[0], d)

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

            else:
                res = build_set_division(nums, d)

                st.subheader("Final Answers")
                st.success(res["answer"])
                st.success(res["not_answer"])

                st.divider()
                st.subheader("Solution")
                st.code(res["steps"], language="text")


if __name__ == "__main__":
    main()
