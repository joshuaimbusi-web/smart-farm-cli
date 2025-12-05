Smart Farm CLI

A fully interactive Command-Line Application for managing farmers, activities, sales, products, buyers, cooperatives, and farmer memberships.
Built with Python, SQLAlchemy ORM, and Alembic for migrations.

The project demonstrates:

Data modeling with SQLAlchemy ORM

Many-to-one, one-to-many, and many-to-many relationships

CLI menu navigation

Database seeding and helpers

Alembic migrations

Clean project structure

Features
✔ Farmers

Create, list, update, delete

Assign activities to farmers

View farmer’s sales

View farmer's cooperatives (many-to-many)

✔ Activities

Activities represent categories of farm operations (e.g., Dairy, Poultry, Crop farming).

Create, list

Link farmers → (one-to-many)

✔ Buyers

Create, list, update, delete

Linked to sales (one-to-many)

✔ Product Types

Catalog of what can be sold: e.g., Milk, Eggs, Vegetables

Create, list

Used when recording sales

✔ Sales

Represents a transaction made by a farmer to a buyer.

Links Farmer → Buyer → ProductType

Stores quantity, price, timestamp

CRUD operations available

✔ Cooperatives (new!)

A farmer can belong to many cooperatives, and a cooperative can have many farmers.

We use an association-object pattern (Membership) so each connection stores metadata:

joined_on

role (Member, Chairperson, Treasurer, etc.)

approved_by

notes

last_updated

CLI menu includes:

List cooperatives

Create cooperative

Link farmer to cooperative

View all memberships

Remove membership

✔ Farmer Activities (Dashboard-style M2M)

Farmers can participate in multiple activities beyond their primary one.

FarmerActivity supports:

extra metadata per link

many-to-many for analytics/dashboards

Project Structure
smart-farm-cli/
│
├── lib/
│   ├── cli.py               # Main CLI application
│   ├── helpers.py           # Input helpers, table printing, session wrapper
│   │
│   ├── db/
│   │   ├── database.py      # SQLAlchemy engine & SessionLocal
│   │   ├── smart_farm.db    # SQLite database (using same path as Alembic)
│   │   └── alembic.ini      # Alembic configuration
│   │
│   ├── models/
│       ├── farmer.py
│       ├── activity.py
│       ├── buyer.py
│       ├── product_type.py
│       ├── sale.py
│       ├── cooperative.py
│       ├── membership.py    # Cooperative ↔ Farmer (association object)
│       ├── farmer_activity.py
│       └── __init__.py      # Imports all models for Alembic autogenerate
│
├── seed.py                   # Database seed script
├── README.md
└── Pipfile / requirements.txt

Database & Migrations
Configured with Alembic

Alembic is configured to point to:

db/smart_farm.db
db/migrations/

Initialize migrations (if needed)
cd db
alembic init migrations

Create a migration
alembic revision --autogenerate -m "initial schema"

Apply migrations
alembic upgrade head

Installation & Setup
1. Create a virtual environment & install dependencies
pip install -r requirements.txt


or if using Pipenv:

pipenv install
pipenv shell

2. Run database migrations
cd db
alembic upgrade head

3. Seed the Database

You can seed using the script:

python seed.py


OR seed through the CLI using the seed option.

4. Start the CLI Application
python -m lib.cli

Using the CLI

The CLI provides structured menus:

Manage Farmers

Manage Activities

Manage Buyers

Manage Product Types

Manage Sales

Farmer Activity (Dashboard)

Cooperatives & Memberships

Each section supports:

Listing

Finding by ID/name

Creating

Updating

Deleting

Viewing relationships

Data is shown in clean table format using the built-in print_table helper.

Development Notes

All DB operations go through a session wrapper:
@with_session(auto_commit=True)

Many-to-many tables use association-object models for flexibility.

Alembic autogenerate works because models/__init__.py imports all models.

The app avoids circular imports by using proper package references (lib.models...).

Requirements

Python 3.10+

SQLAlchemy

Alembic

Tabulate-style table printing (built manually in helpers.py)

SQLite (default)

License

Free to use for learning and educational purposes.