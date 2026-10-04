PYTHON ?= python

.PHONY: install test generate generate-full train evaluate interview pipeline lint

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest

generate:
	$(PYTHON) scripts/generate_data.py --customers 10000 --transactions 100000

generate-full:
	$(PYTHON) scripts/generate_data.py --customers 100000 --transactions 5000000

train:
	$(PYTHON) scripts/train.py

evaluate:
	$(PYTHON) scripts/evaluate.py

interview:
	$(PYTHON) scripts/interview.py --full

pipeline:
	$(PYTHON) scripts/run_pipeline.py

lint:
	$(PYTHON) -m ruff check src tests scripts
