.PHONY: lint ruff

WEB_CONTAINER_NAME=my_currency_web
TEST_WEB_IMAGE_NAME=my_currency_web_test

define clean_docker
	docker stop $(1) || true
	docker rm $(1) || true
	docker image rm $(1):latest || true
endef

define run_test_image_command
	$(call clean_docker, $(TEST_WEB_IMAGE_NAME))
	docker build \
		-f docker/Dockerfile.test \
		--cache-from $(TEST_WEB_IMAGE_NAME) \
		-t $(TEST_WEB_IMAGE_NAME) .
	docker run --rm \
		--env-file envs/test/web.env \
		--name $(TEST_WEB_IMAGE_NAME) \
		$(TEST_WEB_IMAGE_NAME):latest \
		$(1)
	$(call clean_docker, $(TEST_WEB_IMAGE_NAME))
endef

rebuild:
	docker compose -f docker/docker-compose.yml up --build -d

run-all:
	docker compose -f docker/docker-compose.yml up -d

shell-web:
	docker exec -it $(WEB_CONTAINER_NAME) bash

attach-web:
	docker compose -f docker/docker-compose.yml attach web

logs:
	docker compose -f docker/docker-compose.yml logs -f

restart-web:
	docker compose -f docker/docker-compose.yml restart web

stop:
	docker compose -f docker/docker-compose.yml stop

load_fixtures:
	docker compose -f docker/docker-compose.yml exec web bash -c "uv run python3 manage.py loaddata core/fixtures/*"

lint:
	$(call run_test_image_command, make ruff)

ruff:
	uv run ruff check src

pytest:
	uv run pytest src
