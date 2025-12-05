# lib/db/models/__init__.py
from .base import Base

# import all models so they register with Base.metadata
from .activity import Activity
from .farmer import Farmer
from .buyer import Buyer
from .product_type import ProductType
from .sale import Sale
from .farmer_activity import FarmerActivity
from .cooperative import Cooperative
from .membership import Membership

__all__ = [
    "Base",
    "Activity",
    "Farmer",
    "Buyer",
    "ProductType",
    "Sale",
    "FarmerActivity",
    "Cooperative",
    "Membership",
]


def init_db(engine=None):
    """
    Create database tables. If engine is None this will try to import your project's
    database engine using package-relative import. Works both when run as a package
    (python -m lib.db.seed) and when running scripts from project root.
    """
    if engine is None:
        # Try package-relative import first (works when this package is inside `lib.db`)
        try:
            from ..database import engine as _engine  # lib.db.database
        except Exception:
            # Fallback to top-level (if you run code differently)
            from database import engine as _engine
        engine = _engine

    Base.metadata.create_all(engine)
