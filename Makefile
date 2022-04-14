python := python3.10


.PHONY: run
run: X.npy
	$(python) main.py

X.npy:
	$(python) load_data.py
