ENGINE_PATH ?= "../Carcassonne-Engine"
.PHONY: .venv
.venv:
	python3.12 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt
build:
	$(MAKE) -C $(ENGINE_PATH) build-python
load_engine: .venv
	.venv/bin/python -m pip install carcassonne_engine \
	--no-index --find-links=$(ENGINE_PATH)/built_wheels -U
test: load_engine .venv
	.venv/bin/python -m pytest test/ -s
clean:
	-rm -r .venv
realclean: clean
	-rm -r .pytest_cache 
	-rm -r test/__pycache__
