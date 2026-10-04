# Contributing

This laboratory accepts corrections that make an exercise clearer, a test stricter, or a financial definition more careful.

- Keep production logic in `src/`. Notebooks should call it.
- Keep the synthetic-data disclaimer. Do not add claims of professional banking, FinTech, production fraud, production credit, Snowflake, or AWS experience.
- Behavioral prompts keep the placeholders `[YOUR REAL EXAMPLE]`, `[YOUR ACTION]`, and `[YOUR RESULT]`.
- New coding exercises need `problem.md`, `starter.py`, `solution.py`, and `test_solution.py`.
- Do not commit data extracts, model artifacts, or secrets. `.env.example` lists the variable names only.
- Run `pytest` before opening a change. The Python exercise suite executes the reference solutions.

The MIT license is in `LICENSE`.
