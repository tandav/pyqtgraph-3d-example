.PHONY: run
run: X.npy
	python main.py

X.npy:
	python _archive/load_data.py
