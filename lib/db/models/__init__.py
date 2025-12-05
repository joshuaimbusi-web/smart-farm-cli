from .base import Base
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
    if engine is None:
        try:
            from ..database import engine as _engine  
        except Exception:
            from database import engine as _engine
        engine = _engine

    Base.metadata.create_all(engine)
