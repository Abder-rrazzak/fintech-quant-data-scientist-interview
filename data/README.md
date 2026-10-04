# Data

Synthetic tables live here after `python scripts/generate_data.py`.

- `raw/` is the generated extract, including deliberate quality defects.
- `processed/` is reserved for cleaned modeling tables.
- `sample/` holds a small CSV extract that can be read without regenerating the full book.

Do not commit large Parquet extracts. The generator is the source of the data.
