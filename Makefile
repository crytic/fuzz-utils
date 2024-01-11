SHELL := /bin/bash

PY_MODULE := test-generator
TEST_MODULE := tests

# Optionally overriden by the user, if they're using a virtual environment manager.
VENV ?= test-generator

# On Windows, venv scripts/shims are under `Scripts` instead of `bin`.
VENV_BIN := $(VENV)/bin
ifeq ($(OS),Windows_NT)
	VENV_BIN := $(VENV)/Scripts
endif

# Optionally overridden by the user in the `release` target.
BUMP_ARGS :=

# Optionally overridden by the user in the `test` target.
TESTS :=

# If the user selects a specific test pattern to run, set `pytest` to fail fast
# and only run tests that match the pattern.
# Otherwise, run all tests and enable coverage assertions, since we expect
# complete test coverage.
ifneq ($(TESTS),)
	TEST_ARGS := -x -k $(TESTS)
else
	TEST_ARGS :=
endif

.PHONY: all
all:
	@echo "Run my targets individually!"

.PHONY: run
run: $(VENV)/pyvenv.cfg
	@. $(VENV_BIN)/activate && test-generator $(ARGS)

.PHONY: lint
lint: $(VENV)/pyvenv.cfg
	. $(VENV_BIN)/activate && \
		black --check . && \
		pylint $(PY_MODULE) $(TEST_MODULE) 
		# ruff $(ALL_PY_SRCS) && \
		# mypy $(PY_MODULE) && 

.PHONY: reformat
reformat:
	. $(VENV_BIN)/activate && \
		black .

.PHONY: test
	. pytest 

.PHONY: test tests
test tests: $(VENV)/pyvenv.cfg
	. $(VENV_BIN)/activate && \
		pytest $(T) $(TEST_ARGS)

.PHONY: package
package: $(VENV)/pyvenv.cfg
	. $(VENV_BIN)/activate && \
		python3 -m build