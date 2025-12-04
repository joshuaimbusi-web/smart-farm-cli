"""
Seed the smart_farm.db database with initial data.
Run from project root:

python -m lib.db.seed
"""

from datetime import date
from lib.db.database import SessionLocal
from lib.db.models import init_db, Activity, Farmer, Buyer, ProductType, Sale


def seed():
    """Create tables and seed initial data"""
    init_db()  # create tables if they do not exist
    session = SessionLocal()
    try:
        # ---------- Activities ----------
        activity1 = Activity(name="Maize Farming",
                             description="Seasonal maize production.",
                             start_date=date(2024, 1, 1),
                             end_date=date(2024, 6, 30))
        activity2 = Activity(name="Dairy Production",
                             description="Daily milk production.",
                             start_date=date(2024, 1, 1),
                             end_date=date(2024, 12, 31))

        session.add_all([activity1, activity2])
        session.commit()  # ensure IDs are present

        # ---------- Farmers ----------
        # Use activity ids (they exist after commit)
        farmer1 = Farmer(name="John Doe",
                         farm_name="Green Valley Farm",
                         national_id="12345678",
                         phone="0712345678",
                         email="john@example.com",
                         address="Nakuru",
                         activity_id=activity1.id,
                         registration_date=date(2024, 2, 1))
        farmer2 = Farmer(name="Mary Wanjiku",
                         farm_name="Sunrise Farm",
                         national_id="87654321",
                         phone="0798765432",
                         email="mary@example.com",
                         address="Nyeri",
                         activity_id=activity2.id,
                         registration_date=date(2024, 3, 1))

        session.add_all([farmer1, farmer2])
        session.commit()

        # ---------- Buyers ----------
        buyer1 = Buyer(name="FreshMart",
                       organization="FreshMart Ltd",
                       contact_phone="0722000000",
                       contact_email="buy@freshmart.co.ke",
                       address="Nairobi",
                       preferred_payment_method="M-Pesa")
        buyer2 = Buyer(name="AgroBuy",
                       organization="AgroBuy Co.",
                       contact_phone="0733000000",
                       contact_email="orders@agrobuy.com",
                       address="Eldoret",
                       preferred_payment_method="Bank Transfer")

        session.add_all([buyer1, buyer2])
        session.commit()

        # ---------- Product Types ----------
        maize = ProductType(name="Maize Grain",
                            category="Cereal",
                            typical_unit="KG",
                            description="Harvested maize grain")
        milk = ProductType(name="Fresh Milk",
                           category="Dairy",
                           typical_unit="Litre",
                           description="Raw fresh milk")

        session.add_all([maize, milk])
        session.commit()

        # ---------- Sales ----------
        sale1 = Sale(farmer_id=farmer1.id,
                     buyer_id=buyer1.id,
                     product_type_id=maize.id,
                     quantity=200,
                     price=45000)
        sale2 = Sale(farmer_id=farmer2.id,
                     buyer_id=buyer2.id,
                     product_type_id=milk.id,
                     quantity=500,
                     price=30000)

        session.add_all([sale1, sale2])
        session.commit()

        print("Database seeded successfully!")
    except Exception as exc:
        # rollback so partial data is not committed in case of an error
        try:
            session.rollback()
        except Exception:
            pass
        print("Error seeding database:", exc)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
