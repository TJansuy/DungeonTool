HOST=0.0.0.0
PORT=42069

all:
	flask run --host $(HOST) --port $(PORT)
