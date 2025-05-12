
.PHONY: setup env test build assets

setup: env assets

env:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

test:
	./venv/bin/pytest -q

build:
	./venv/bin/python setup.py sdist bdist_wheel

assets:
	./venv/bin/python -m resonance_sandbox.scripts.generate_assets
