"""
Run quick database checks without using the CLI.
Use:  python debug.py
"""

from lib.db import models
from lib.db.database import SessionLocal

def main():
    models.init_db()  # ensure schema exists
    session = SessionLocal()

    print("=== Debug DB ===")

    # Example queries:
    print("\nFarmers:")
    for f in models.Farmer.get_all(session):
        print(f.id, f.name, f.national_id)

    print("\nBuyers:")
    for b in models.Buyer.get_all(session):
        print(b.id, b.name)

    print("\nProduct Types:")
    for p in models.ProductType.get_all(session):
        print(p.id, p.name)

    print("\nSales:")
    for s in models.Sale.get_all(session):
        print(
            s.id,
            "|",
            s.farmer.name if s.farmer else "NoFarmer",
            "->",
            s.buyer.name if s.buyer else "NoBuyer",
            "|",
            (s.product_type.name if s.product_type else "NoProduct"),
            "| Qty:", s.quantity,
            "| Price:", s.price,
        )

    session.close()


if __name__ == "__main__":
    main()
