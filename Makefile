HTTP_PORT ?= 8000
run:
	docker compose run --rm -p $(HTTP_PORT):$(HTTP_PORT) http_proxy 
build: 
	docker compose build