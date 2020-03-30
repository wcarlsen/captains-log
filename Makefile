install:
	pipenv install

install_dev:
	pipenv install --dev

run:
	pipenv run start

test: flake8 black mypy pytest

flake8:
	@echo "\n# Flake8\n"
	pipenv run flake8 service.py src

mypy:
	@echo "\n# Mypy\n"
	pipenv run mypy --ignore-missing-imports service.py src

make pytest:
	@echo "\n# Pytest\n"
	pipenv run pytest

make black:
	@echo "\n# Black\n"
	pipenv run black --check src tests

build:
	docker build . -t captains-log:latest