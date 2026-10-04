"""Transaction-focused entry point.

Writes the full consistent laboratory (dimensions plus facts). A transaction
file without customers, accounts, and merchants cannot support point-in-time
features or referential checks.
"""

from generate_data import main

if __name__ == "__main__":
    main()
