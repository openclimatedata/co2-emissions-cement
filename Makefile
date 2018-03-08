all: data/co2-emissions-cement.csv

download: scripts/download.py venv
	@echo $@
	@./venv/bin/python $<

data/co2-emissions-cement.csv data/unfccc-2017.csv: scripts/process.py venv
	@./venv/bin/python $<

venv: scripts/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur scripts/requirements.txt
	touch venv

clean:
	rm -rf data/*.csv

clean-venv:
	rm -rf venv

.PHONY: clean download
