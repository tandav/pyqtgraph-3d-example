python := python3.10


.PHONY: run
run: X.npy
	MIDI_DEVICE='IAC Driver Bus 1' $(python) main.py

X.npy:
	$(python) load_data.py
