source_dir := $(CURDIR)/src
source_files := $(shell find $(source_dir) -type f -name "*.py")
tests_dir := $(CURDIR)/tests
build_dir := $(CURDIR)/build
dist_dir := $(CURDIR)/dist

ENV_NAME = env
PYTHON_COMMAND ?= python
make_env = $(PYTHON_COMMAND) -m venv $(ENV_NAME)
env_dir = $(CURDIR)/$(ENV_NAME)
bin_dir = $(env_dir)/bin
activate_env = . $(bin_dir)/activate
PYTHONPATH = $(source_dir):$(ODOO_COMMUNITY_PATH)

PYTEST_FILE_OR_DIR ?= tests
pytest_temp_files := .coverage .pytest_cache

define create-env
	@echo Creating $@...
	$(make_env)
	$(bin_dir)/pip install --upgrade pip
	$(bin_dir)/pip install pip-tools
endef

define clear-python-cache
	@echo Clearing Python cache...
	rm -rf `find . -type d -name ".cache"`
	rm -rf `find . -type d -name "__pycache__"`
	rm -rf `find . -type f -name "*.py[co]"`
	rm -rf `find . -type d -name "*.egg-info"`
	rm -rf `find . -type d -name "pip-wheel-metadata"`
endef

.PHONY: all
all: install test

env:
	$(create-env)

.PHONY: install
install: env
	$(bin_dir)/pip-sync requirements.txt dev-requirements.txt

.PHONY: lint
lint:
	$(bin_dir)/flake8 $(source_dir)

.PHONY: format
format:
	$(bin_dir)/black $(source_dir)

.PHONY: test
test: lint
	PYTHONPATH="$(PYTHONPATH)" 					\
	$(bin_dir)/pytest -vvs 						\
		--cov=$(source_dir) 					\
		--cov-report term-missing 				\
		--cov-fail-under 0 						\
		$(PYTEST_FILE_OR_DIR)

.PHONY: verify
verify:
	$(bin_dir)/python setup.py verify

dist:
	$(bin_dir)/python setup.py sdist
	$(bin_dir)/python setup.py bdist_wheel

.PHONY: verify
upload: dist
	$(bin_dir)/twine upload $(dist_dir)/*

.PHONY: clean
clean:
	rm -rf $(env_dir) $(pytest_temp_files) $(build_dir) $(dist_dir)
	$(clear-python-cache)
