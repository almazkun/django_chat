REGISTRY=ghcr.io/almazkun
IMAGE_NAME=django-chat
CONTAINER_NAME=django-chat-container
VERSION=latest


lint:
	pipenv run isort --recursive --force-single-line-imports --line-width 999 .
	pipenv run autoflake --recursive --ignore-init-module-imports --in-place --remove-all-unused-imports .
	pipenv run isort --recursive --use-parentheses --trailing-comma --multi-line 3 --force-grid-wrap 0 --line-width 140 .
	pipenv run black .
	djlint . --reformat

build:
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .

push:
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

run:
	docker run \
		-it \
		--rm \
		-d \
		-p 8000:8000 \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		$(REGISTRY)/$(IMAGE_NAME):$(VERSION)

stop:
	docker stop $(CONTAINER_NAME)

pull:
	docker pull $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
