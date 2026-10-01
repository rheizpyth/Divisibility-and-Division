"""
Divisibility and Division of Integers (standalone).
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
# Math / solution builders
# =====================================================================
def paren(n: int) -> str:
    """Wraps negative numbers in parentheses so signs never collide."""
    return f"({n})" if n < 0 else str(n)


def division_algorithm(a: int, d: int) -> tuple:
    """Returns (q, r) with a = q(d) + r and 0 <= r < |d|. Works for negative a and d."""
    r = a % abs(d)
    q = (a - r) // d
    return q, r


def division_lines(a: int, d: int) -> tuple:
    """Step-by-step Division Algorithm for a divided by d. Returns (lines, q, r)."""
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


def divisibility_lines(a: int, d: int, q: int, r: int) -> tuple:
    """Does d divide a? Returns (lines, answer)."""
    if r == 0:
        return (
            [
                f"The remainder is r = 0, so {d} divides {a}.",
                f"{a} = {paren(q)}({d})",
                f"Therefore {d} | {a}  ({a} is a multiple of {d}).",
            ],
            f"{d} | {a}  (q = {q})",
        )
    return (
        [
            f"The remainder is r = {r}, which is not 0.",
            f"Therefore {d} does not divide {a}.",
        ],
        f"{d} does not divide {a}",
    )


def solve_single(a: int, d: int) -> dict:
    lines, q, r = division_lines(a, d)
    divis_lines, divis_answer = divisibility_lines(a, d, q, r)
    return {
        "title": f"Dividing {a} by {d}",
        "answers": [f"{a} = {paren(q)}({d}) + {r}   (q = {q}, r = {r})", divis_answer],
        "sections": [
            ("Division Algorithm Solution", "\n".join(lines)),
            ("Divisibility", "\n".join(divis_lines)),
        ],
    }


def solve_set(numbers: list, d: int) -> dict:
    lines = [f"Divisor d = {d}, |d| = {abs(d)}, so 0 <= r < {abs(d)}", ""]
    divisible, not_divisible = [], []

    for a in numbers:
        q, r = division_algorithm(a, d)
        verdict = f"{d} | {a}" if r == 0 else f"{d} does not divide {a}"
        lines.append(f"{a} = {paren(q)}({d}) + {r}   ->  {verdict}")
        (divisible if r == 0 else not_divisible).append(a)

    fmt = lambda xs: "{" + (", ".join(map(str, xs)) if xs else "none") + "}"
    return {
        "title": f"Dividing the set {fmt(numbers)} by {d}",
        "answers": [
            f"Divisible by {d}: {fmt(divisible)}",
            f"Not divisible by {d}: {fmt(not_divisible)}",
        ],
        "sections": [("Solution", "\n".join(lines))],
    }


def solve_divisors(n: int) -> dict:
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
    everything = sorted([-p for p in positive] + positive)
    return {
        "title": f"Divisors of {n}",
        "answers": [
            f"Positive divisors of {m}: {', '.join(map(str, positive))}",
            f"All divisors of {n}: {', '.join(map(str, everything))}",
        ],
        "sections": [("Solution (testing each i up to the square root of |n|)", "\n".join(lines))],
    }


# =====================================================================
# Input parsing
# =====================================================================
def parse_numbers(text: str) -> list:
    return [int(piece) for piece in text.replace(",", " ").split()]


def solve_query(query: str) -> dict:
    """Reads the search bar text and returns a solution dict. Raises ValueError on bad input."""
    text = query.strip().replace("÷", "/")
    if not text:
        raise ValueError("Type something in the search bar first.")

    # divisors 36
    if text.lower().startswith("divisors"):
        nums = parse_numbers(text[len("divisors"):])
        if len(nums) != 1 or nums[0] == 0:
            raise ValueError("Use: divisors n   (one nonzero integer), e.g. divisors 36")
        return solve_divisors(nums[0])

    # 5 | 10 20 33     (d divides each number in the set)
    if "|" in text:
        left, right = text.split("|", 1)
        try:
            ds, nums = parse_numbers(left), parse_numbers(right)
        except ValueError:
            raise ValueError("Use whole numbers only, e.g. 5 | 20")
        if len(ds) != 1 or not nums:
            raise ValueError("Use: d | a   or   d | a b c ...   e.g. 5 | 10 20 33")
        if ds[0] == 0:
            raise ValueError("The divisor cannot be zero.")
        return solve_single(nums[0], ds[0]) if len(nums) == 1 else solve_set(nums, ds[0])

    # -17 / 5   or   12 -17 25 40 / 5
    if "/" in text:
        left, right = text.rsplit("/", 1)
        try:
            nums, ds = parse_numbers(left), parse_numbers(right)
        except ValueError:
            raise ValueError("Use whole numbers only, e.g. -17 / 5")
        if len(ds) != 1 or not nums:
            raise ValueError("Use: a / d   or   a b c ... / d   e.g. 12 -17 25 / 5")
        if ds[0] == 0:
            raise ValueError("The divisor cannot be zero.")
        return solve_single(nums[0], ds[0]) if len(nums) == 1 else solve_set(nums, ds[0])

    raise ValueError("Use  a / d,  a b c / d,  d | a,  or  divisors n.")


# =====================================================================
# Streamlit UI
# =====================================================================
def main():
    import streamlit as st

    st.title("Divisibility and Division of Integers")
    st.write("Division Algorithm (a = qd + r, 0 <= r < |d|), divisibility tests, and divisors.")

    query = st.text_input(
        "Search bar",
        placeholder="e.g.  -17 / 5   |   12 -17 25 40 / 5   |   5 | 20   |   divisors 36",
    )
    st.caption(
        "a / d: divide.  a b c / d: divide a set.  d | a: does d divide a?  divisors n: list divisors."
    )

    if st.button("Calculate"):
        try:
            sol = solve_query(query)
        except ValueError as err:
            st.error(str(err))
            st.stop()

        st.subheader(sol["title"])
        st.subheader("Final Answers")
        for ans in sol["answers"]:
            st.success(ans)

        for heading, body in sol["sections"]:
            st.divider()
            st.subheader(heading)
            st.code(body, language="text")


if __name__ == "__main__":
    main()
else:
    # Streamlit runs the script with __name__ == "__main__"; this branch covers
    # `streamlit run` variants that import the module instead.
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is not None:
            main()
    except Exception:
        pass
