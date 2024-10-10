ENGINE_PATH ?= "../Carcassonne-Engine"
build:
	$(MAKE) -C $(ENGINE_PATH) build-python

.PHONY: .venv
.venv:
	python3.12 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/python -m pip install carcassonne_engine \
	--no-index --find-links=$(ENGINE_PATH)/built_wheels \
	--force-reinstall -U
test: build .venv
	.venv/bin/python -m pytest test/ -s -m 'not slow'
test-slow: build .venv
	.venv/bin/python -m pytest test/ -s -m slow
clean:
	-rm -r .venv
realclean: clean
	-rm -r .pytest_cache 
	-rm -r test/__pycache__
