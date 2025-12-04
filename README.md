# Farm Market CLI

A CLI application demonstrating an ORM-backed app using SQLAlchemy. Models:
- Activity (one-to-many -> Farmer)
- Farmer (many-to-one Activity, one-to-many Sale)
- Buyer (one-to-many Sale)
- ProductType (catalog)
- Sale (links Farmer, Buyer, ProductType and stores quantity & price)

Run the app:
1. Create a virtualenv and install dependencies (pipenv or pip).
2. Seed the DB: `python -m lib.cli`. or run the CLI and choose seed option.
3. Start the CLI: `python -m lib.cli`.

The CLI supports create/list/view/find/delete operations for each model and viewing related objects.
