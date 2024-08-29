clean:
	rm -rf .venv uv.lock htmlcov .coverage .sesskey

install-python:
	uv python install 3.12


# Dev
run-dev: install-python
	uv run uvicorn --host 0.0.0.0 app.main:app --reload


# Use these for local development without Docker.
.venv/bin/activate: pyproject.toml
	uv venv

venv-install-dev: .venv/bin/activate
	. .venv/bin/activate && uv pip install .[test,lint,debug]

venv-run-dev: venv-install-dev
	. .venv/bin/activate && python main.py

venv-cov: venv-install-dev
	. .venv/bin/activate \
	&& coverage run --branch --source=app -m pytest -ssvv tests \
	&& coverage report -m --fail-under=90

venv-mypy: venv-install-dev
	. .venv/bin/activate && mypy --strict app tests  # Why "." is not working? ):

venv-ruff-check: venv-install-dev
	. .venv/bin/activate && ruff check .

venv-ruff-fix: venv-install-dev
	. .venv/bin/activate && ruff check . --fix

venv-ruff-format: venv-install-dev
	. .venv/bin/activate && ruff format

venv-lint: venv-install-dev
	. .venv/bin/activate \
	&& ruff check app tests \
	&& ruff format --check . \
	&& mypy --strict app tests  # Why "." is not working? ):
