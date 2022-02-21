# Service definitions
export PYTHONPATH := .:src:$(PYTHONPATH)

SERVICE=src/
UNIT_TESTS=tests/unit

# Run test out of Poetry env
ifeq ($(CICD), TRUE)
	PYTEST_FLAGS = -p no:warnings
else
	POETRY_ARG = poetry run
	PYTEST_FLAGS = -v
endif

## Scripts to run tests

static-tests:
	###### Running style analysis ######
	$(POETRY_ARG) flake8 $(SERVICE)
	###### Running static type analysis ######
	$(POETRY_ARG) mypy $(SERVICE)
	###### Running documentation analysis ######
	$(POETRY_ARG) pydocstyle $(SERVICE)

unit-tests:
	###### Running unit tests with coverage analysis with JUnit xml export ######
	$(POETRY_ARG) pytest $(PYTEST_FLAGS) $(UNIT_TESTS) --cov --cov-report xml --junitxml coverage.xml --cov-report term

tests: static-tests unit-tests

## Scripts to run Docker commands

docker-build:
	###### Docker build the API service ######
	docker build --rm --tag api:dev --target production .

docker-run:
	###### Docker run the API service ######
	docker run --name api-dev -p 5000:5000 --rm api:dev

docker-stop:
	###### Docker stop the API service ######
	docker stop api-dev

docker-test:
	###### Docker build and run tests ######
	docker build --rm --tag api:test --target tester .
	docker run --name api-test --rm api:test

## Scripts to help development

api:
	$(POETRY_ARG) uvicorn src.main:app --no-access-log --log-level info --host 0.0.0.0 --port 5000 --reload --reload-dir src
