install:
	pipenv install

install_dev:
	pipenv install --dev

run:
	pipenv run start

test: mypy flake8

flake8:
	@echo "\n# Flake8\n"
	pipenv run flake8 service.py src

mypy:
	@echo "\n# Mypy\n"
	pipenv run mypy --ignore-missing-imports service.py src

build:
	docker build . -t captains-log:latest