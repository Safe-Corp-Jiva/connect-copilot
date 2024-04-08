all: dev

dev-build: dev.dockerfile
	docker build -t stream/copilot -f dev.dockerfile .

dev: dev-build
	docker compose up -d

start:
	docker compose up -d

stop:
	docker compose pause

clean:
	docker compose down