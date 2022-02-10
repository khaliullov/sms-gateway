DOCKER_COMPOSE_OPTS :=

.PHONY: all run up

.EXPORT_ALL_VARIABLES:

-include .env

ifneq ($(START_GAMMU), 0)
	DOCKER_COMPOSE_OPTS := ${DOCKER_COMPOSE_OPTS} -f docker-compose.devices.yml
endif

all: run

.env:
	@echo ".env file was not found, creating with defaults. Please rerun"
	cp .env.dist .env
	exit 1

run: .env # run locally
	python3 ./src/main.py

up: # bring up docker-compose
	docker-compose -f docker-compose.yml ${DOCKER_COMPOSE_OPTS} up -d
