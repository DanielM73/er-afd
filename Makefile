PYTHON ?= python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip
ER ?= (a|b)*abb
CADENA ?= abb

.PHONY: config build run test clean

config:
	$(PYTHON) -m venv $(VENV)

build: config
	$(VENV_PIP) install -e .
	$(VENV_PYTHON) -m compileall -q er_afd

run:
	@$(VENV_PYTHON) -m er_afd "$(ER)" "$(CADENA)"; codigo=$$?; \
	if [ $$codigo -eq 0 ] || [ $$codigo -eq 1 ]; then exit 0; else exit $$codigo; fi

test:
	$(VENV_PYTHON) -m unittest discover -s tests -v

clean:
	rm -rf $(VENV) .pytest_cache build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

