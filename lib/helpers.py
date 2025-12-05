from functools import wraps
from typing import Callable, Optional, Tuple
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from lib.db.database import SessionLocal
from lib.db.models import Membership  

def with_session(auto_commit: bool = False):
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
    if not rows:
        print("\n(no records found)\n")
        return

    rows = [[str(cell) for cell in row] for row in rows]
    headers = [str(h) for h in headers]
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
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty")


def input_optional(prompt: str) -> Optional[str]:
    v = input(prompt).strip()
    return v if v != "" else None


def input_confirm(prompt: str, default: bool = False) -> bool:
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
    while True:
        v = input(prompt).strip()
        try:
            return int(v)
        except ValueError:
            print("Please enter a valid integer")

def input_float(prompt: str) -> float:
    while True:
        v = input(prompt).strip()
        try:
            return float(v)
        except ValueError:
            print("Please enter a valid number")


def input_date(prompt: str) -> Optional[date]:
    while True:
        v = input(prompt).strip()
        if v == "":
            return None
        try:
            return datetime.fromisoformat(v).date()
        except Exception:
            print("Please enter a valid date in YYYY-MM-DD format or leave blank.")

def safe_add_membership(session, farmer, coop, role: str = "Member") -> Tuple[Optional[Membership], bool]:
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
        existing = session.query(Membership).filter_by(farmer_id=farmer.id, cooperative_id=coop.id).first()
        return existing, False
