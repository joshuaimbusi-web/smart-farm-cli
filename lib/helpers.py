# lib/helpers.py
from functools import wraps
from typing import Callable, Optional, Tuple
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError

# Import the session factory from your database module (package layout)
from lib.db.database import SessionLocal
from lib.db.models import Membership  # used by safe_add_membership


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


def input_optional(prompt: str) -> Optional[str]:
    """
    Prompt for an optional string. Returns None if the user enters blank,
    otherwise returns the stripped string.
    """
    v = input(prompt).strip()
    return v if v != "" else None


def input_confirm(prompt: str, default: bool = False) -> bool:
    """
    Ask a yes/no question. Returns True for yes, False for no.
    default controls what happens on blank input.
    """
    yes = {"y", "yes"}
    no = {"n", "no"}
    default_str = "Y/n" if default else "y/N"
    while True:
        v = input(f"{prompt} ({default_str}): ").strip().lower()
        if v == "":
            return default
        if v in yes:
            return True
        if v in no:
            return False
        print("Please enter Y or N.")


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


# -------------------------
# Convenience DB helpers
# -------------------------
def safe_add_membership(session, farmer, coop, role: str = "Member") -> Tuple[Optional[Membership], bool]:
    """
    Safely add a Membership linking farmer <-> coop.
    Returns (membership_obj, created_bool).
    If a membership already exists, returns (existing_obj, False).
    On success returns (new_obj, True).
    """
    existing = session.query(Membership).filter_by(farmer_id=farmer.id, cooperative_id=coop.id).first()
    if existing:
        return existing, False

    m = Membership(farmer=farmer, cooperative=coop, role=role, joined_on=date.today())
    session.add(m)
    try:
        session.commit()
        return m, True
    except IntegrityError:
        session.rollback()
        # someone else might have created it concurrently; fetch and return
        existing = session.query(Membership).filter_by(farmer_id=farmer.id, cooperative_id=coop.id).first()
        return existing, False
