from functools import wraps
from typing import Callable, Optional
from datetime import date, datetime

# Import the session factory from your database module (adjusted to package layout)
from lib.db.database import SessionLocal


def with_session(auto_commit: bool = False):
    """
    Decorator factory returning a decorator that provides a DB session as the
    first argument to the wrapped function.

    Usage:
        @with_session()
        def fn(session, ...):
            ...

    If auto_commit=True, the decorator will commit the session when the wrapped
    function returns successfully; otherwise commit is left to the function.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = SessionLocal()
            try:
                result = func(session, *args, **kwargs)
                if auto_commit:
                    session.commit()
                return result
            except Exception:
                # ensure DB state is reset so subsequent operations can continue
                try:
                    session.rollback()
                except Exception:
                    pass
                raise
            finally:
                session.close()
        return wrapper
    return decorator


def print_table(rows, headers):
    """
    Lightweight table printer that uses only Python stdlib.
    rows: iterable of iterables (tuples/lists)
    headers: list of column names
    """
    if not rows:
        print("\n(no records found)\n")
        return

    # Ensure rows are lists of strings
    rows = [[str(cell) for cell in row] for row in rows]
    headers = [str(h) for h in headers]

    # Compute max width per column
    columns = list(zip(*([headers] + rows)))
    col_widths = [max(len(v) for v in col) + 2 for col in columns]  # padding

    fmt = "".join("{:<" + str(w) + "}" for w in col_widths)

    print()
    print(fmt.format(*headers))
    print("-" * sum(col_widths))
    for row in rows:
        print(fmt.format(*row))
    print()


def input_nonempty(prompt: str) -> str:
    """Prompt until a non-empty input is entered."""
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty")


def input_int(prompt: str) -> int:
    """Prompt until a valid integer is entered."""
    while True:
        v = input(prompt).strip()
        try:
            return int(v)
        except ValueError:
            print("Please enter a valid integer")


def input_float(prompt: str) -> float:
    """Prompt until a valid number (float) is entered."""
    while True:
        v = input(prompt).strip()
        try:
            return float(v)
        except ValueError:
            print("Please enter a valid number")


def input_date(prompt: str) -> Optional[date]:
    """
    Prompt for a date in YYYY-MM-DD format.
    Returns a datetime.date or None if user enters blank.
    Keeps prompting until input is blank or a valid date.
    """
    while True:
        v = input(prompt).strip()
        if v == "":
            return None
        try:
            # Use fromisoformat which accepts YYYY-MM-DD
            return datetime.fromisoformat(v).date()
        except Exception:
            print("Please enter a valid date in YYYY-MM-DD format or leave blank.")
