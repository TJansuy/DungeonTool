HOST=0.0.0.0
PORT=42070

all:
	flask run --host $(HOST) --port $(PORT)
