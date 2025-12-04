"""Simple menu-driven CLI. Entry: python -m lib.cli"""

from lib.helpers import (
    with_session,
    print_table,
    input_nonempty,
    input_int,
    input_float,
    input_date,
)

# import your multi-file model package as "db"
from lib.db.models import (
    init_db,
    Activity,
    Farmer,
    Buyer,
    ProductType,
    Sale,
)


def main_menu():
    print("\n=== Smart Farm CLI ===")
    print("1) Activities")
    print("2) Farmers")
    print("3) Buyers")
    print("4) Product Types")
    print("5) Sales")
    # print("6) Seed DB (sample data)")
    print("0) Exit")


# -----------------------------
# ACTIVITIES
# -----------------------------

@with_session()
def activities_menu(session):
    while True:
        print("\n-- Activities --")
        print("1) Create Activity")
        print("2) List Activities")
        print("3) View Activity (by id)")
        print("4) Delete Activity")
        print("0) Back")
        choice = input("> ").strip()

        if choice == "1":
            name = input_nonempty("Name: ")
            desc = input("Description: ") or None
            sd = input_date("Start date (YYYY-MM-DD) or blank: ")
            ed = input_date("End date (YYYY-MM-DD) or blank: ")

            kwargs = {"name": name, "description": desc}
            if sd:
                kwargs["start_date"] = sd
            if ed:
                kwargs["end_date"] = ed

            try:
                a = Activity.create(session, **kwargs)
                print("Created", a.id, a.name)
            except Exception as e:
                print("Error creating activity:", e)

        elif choice == "2":
            rows = [
                (a.id, a.name, a.start_date, a.end_date)
                for a in Activity.get_all(session)
            ]
            print_table(rows, ["id", "name", "start", "end"])

        elif choice == "3":
            id_ = input_int("Activity id: ")
            a = Activity.find_by_id(session, id_)
            if not a:
                print("Not found")
            else:
                print(f"{a.id} - {a.name}\nDesc: {a.description}\nFarmers:")
                rows = [(f.id, f.name, f.farm_name) for f in a.farmers]
                print_table(rows, ["id", "name", "farm"])

        elif choice == "4":
            id_ = input_int("Activity id to delete: ")
            a = Activity.find_by_id(session, id_)
            if not a:
                print("Not found")
            else:
                confirm = input(f"Confirm delete activity {a.name}? (y/N): ").lower()
                if confirm == "y":
                    a.delete(session)
                    print("Deleted")

        elif choice == "0":
            break
        else:
            print("Invalid option")


# -----------------------------
# FARMERS
# -----------------------------

@with_session()
def farmers_menu(session):
    while True:
        print("\n-- Farmers --")
        print("1) Create Farmer")
        print("2) List Farmers")
        print("3) View Farmer")
        print("4) Find Farmer by name")
        print("5) Delete Farmer")
        print("0) Back")
        c = input("> ").strip()

        if c == "1":
            name = input_nonempty("Name: ")
            farm_name = input("Farm name: ").strip() or None
            national_id = input_nonempty("National ID: ")
            phone = input("Phone: ").strip() or None
            email = input("Email: ").strip() or None

            activity_id = input("Activity id (optional): ").strip() or None

            kwargs = dict(
                name=name,
                farm_name=farm_name,
                national_id=national_id,
                phone=phone,
                email=email,
            )

            if activity_id.isdigit():
                kwargs["activity_id"] = int(activity_id)

            try:
                f = Farmer.create(session, **kwargs)
                print("Created farmer", f.id)
            except Exception as e:
                print("Error:", e)

        elif c == "2":
            rows = [
                (
                    f.id,
                    f.name,
                    f.national_id,
                    f.activity.name if f.activity else "",
                )
                for f in Farmer.get_all(session)
            ]
            print_table(rows, ["id", "name", "nat_id", "activity"])

        elif c == "3":
            id_ = input_int("Farmer id: ")
            f = Farmer.find_by_id(session, id_)
            if not f:
                print("Not found")
            else:
                print(
                    f"{f.id} - {f.name} ({f.farm_name})\n"
                    f"Contact: {f.phone} / {f.email}\nSales:"
                )
                rows = [
                    (
                        s.id,
                        s.buyer.name if s.buyer else "-",
                        s.product_type.name if s.product_type else "-",
                        s.quantity,
                        s.price,
                        s.created_at,
                    )
                    for s in f.sales
                ]
                print_table(rows, ["id", "buyer", "product", "qty", "price", "date"])

        elif c == "4":
            q = input_nonempty("Search name: ")
            rows = [(f.id, f.name) for f in Farmer.find_by_name(session, q)]
            print_table(rows, ["id", "name"])

        elif c == "5":
            id_ = input_int("Farmer id to delete: ")
            f = Farmer.find_by_id(session, id_)
            if not f:
                print("Not found")
            else:
                if input("Confirm delete (y/N): ").lower() == "y":
                    f.delete(session)
                    print("Deleted")

        elif c == "0":
            break
        else:
            print("Invalid option")


# -----------------------------
# BUYERS
# -----------------------------

@with_session()
def buyers_menu(session):
    while True:
        print("\n-- Buyers --")
        print("1) Create Buyer")
        print("2) List Buyers")
        print("3) View Buyer")
        print("4) Delete Buyer")
        print("0) Back")
        c = input("> ").strip()

        if c == "1":
            name = input_nonempty("Name: ")
            org = input("Organization: ").strip() or None
            phone = input("Phone: ").strip() or None
            email = input("Email: ").strip() or None
            addr = input("Address: ").strip() or None

            b = Buyer.create(
                session,
                name=name,
                organization=org,
                contact_phone=phone,
                contact_email=email,
                address=addr,
            )
            print("Created buyer", b.id)

        elif c == "2":
            rows = [(b.id, b.name, b.organization) for b in Buyer.get_all(session)]
            print_table(rows, ["id", "name", "org"])

        elif c == "3":
            id_ = input_int("Buyer id: ")
            b = Buyer.find_by_id(session, id_)
            if not b:
                print("Not found")
            else:
                print(f"{b.id} - {b.name}\nSales:")
                rows = [
                    (
                        s.id,
                        s.farmer.name if s.farmer else "-",
                        s.product_type.name if s.product_type else "-",
                        s.quantity,
                        s.price,
                        s.created_at,
                    )
                    for s in b.sales
                ]
                print_table(rows, ["id", "farmer", "product", "qty", "price", "date"])

        elif c == "4":
            id_ = input_int("Buyer id to delete: ")
            b = Buyer.find_by_id(session, id_)
            if not b:
                print("Not found")
            else:
                if input("Confirm delete (y/N): ").lower() == "y":
                    b.delete(session)
                    print("Deleted")

        elif c == "0":
            break
        else:
            print("Invalid option")


# -----------------------------
# PRODUCT TYPES
# -----------------------------

@with_session()
def products_menu(session):
    while True:
        print("\n-- Product Types --")
        print("1) Create Product Type")
        print("2) List Product Types")
        print("3) View Product Type")
        print("4) Delete Product Type")
        print("0) Back")
        c = input("> ").strip()

        if c == "1":
            name = input_nonempty("Name: ")
            cat = input("Category: ").strip() or None
            unit = input("Typical unit: ").strip() or None
            desc = input("Description: ").strip() or None

            p = ProductType.create(
                session, name=name, category=cat, typical_unit=unit, description=desc
            )
            print("Created", p.id)

        elif c == "2":
            rows = [
                (p.id, p.name, p.category, p.typical_unit)
                for p in ProductType.get_all(session)
            ]
            print_table(rows, ["id", "name", "category", "unit"])

        elif c == "3":
            id_ = input_int("Product id: ")
            p = ProductType.find_by_id(session, id_)
            if not p:
                print("Not found")
            else:
                print(f"{p.id} - {p.name}\n{p.description}\nSales:")
                rows = [
                    (
                        s.id,
                        s.farmer.name if s.farmer else "-",
                        s.buyer.name if s.buyer else "-",
                        s.quantity,
                        s.price,
                        s.created_at,
                    )
                    for s in p.sales
                ]
                print_table(rows, ["id", "farmer", "buyer", "qty", "price", "date"])

        elif c == "4":
            id_ = input_int("Product id to delete: ")
            p = ProductType.find_by_id(session, id_)
            if not p:
                print("Not found")
            else:
                if input("Confirm delete (y/N): ").lower() == "y":
                    p.delete(session)
                    print("Deleted")

        elif c == "0":
            break
        else:
            print("Invalid option")


# -----------------------------
# SALES
# -----------------------------

@with_session()
def sales_menu(session):
    while True:
        print("\n-- Sales --")
        print("1) Create Sale")
        print("2) List Sales")
        print("3) View Sale")
        print("4) Delete Sale")
        print("0) Back")
        c = input("> ").strip()

        if c == "1":
            farmer_id = input_int("Farmer id: ")
            buyer_id = input_int("Buyer id: ")
            product_id = input("Product id (optional): ").strip()
            quantity = input_float("Quantity: ")
            price = input_float("Price: ")

            farmer = Farmer.find_by_id(session, farmer_id)
            buyer = Buyer.find_by_id(session, buyer_id)

            product = None
            if product_id.isdigit():
                product = ProductType.find_by_id(session, int(product_id))

            if not farmer or not buyer:
                print("Farmer or buyer not found")
            else:
                s = Sale.create(
                    session,
                    farmer=farmer,
                    buyer=buyer,
                    product_type=product,
                    quantity=quantity,
                    price=price,
                )
                print("Created sale", s.id)

        elif c == "2":
            rows = [
                (
                    s.id,
                    s.farmer.name if s.farmer else "-",
                    s.buyer.name if s.buyer else "-",
                    s.product_type.name if s.product_type else "-",
                    s.quantity,
                    s.price,
                    s.created_at,
                )
                for s in Sale.get_all(session)
            ]
            print_table(rows, ["id", "farmer", "buyer", "product", "qty", "price", "date"])

        elif c == "3":
            id_ = input_int("Sale id: ")
            s = Sale.find_by_id(session, id_)
            if not s:
                print("Not found")
            else:
                print(
                    f"Sale {s.id}: Farmer={s.farmer.name if s.farmer else 'N/A'} "
                    f"Buyer={s.buyer.name if s.buyer else 'N/A'} "
                    f"Product={s.product_type.name if s.product_type else 'N/A'} "
                    f"Qty={s.quantity} Price={s.price} Date={s.created_at}"
                )

        elif c == "4":
            id_ = input_int("Sale id to delete: ")
            s = Sale.find_by_id(session, id_)
            if not s:
                print("Not found")
            else:
                if input("Confirm delete (y/N): ").lower() == "y":
                    s.delete(session)
                    print("Deleted")

        elif c == "0":
            break
        else:
            print("Invalid option")


# -----------------------------
# MAIN LOOP
# -----------------------------

def main():
    init_db()  # creates tables

    while True:
        main_menu()
        choice = input("> ").strip()

        if choice == "1":
            activities_menu()
        elif choice == "2":
            farmers_menu()
        elif choice == "3":
            buyers_menu()
        elif choice == "4":
            products_menu()
        elif choice == "5":
            sales_menu()
        elif choice == "6":
            # optional seeding
            from lib.db import seed as seed_module
            seed_module.seed()
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
