DOCKER_ORG := ga4gh
DOCKER_REPO := refget-compliance-suite
DOCKER_TAG := $(shell cat setup.py | grep "version" | cut -f 2 -d '"')
DOCKER_IMG := ${DOCKER_ORG}/${DOCKER_REPO}:${DOCKER_TAG}
DOCKER_FILE := Dockerfile

# default
.PHONY: Nothing
Nothing:
	@echo "No target provided. Stop"

# build docker image
.PHONY: docker-build
docker-build: $(DOCKER_FILE)
	docker build -t $(DOCKER_IMG) --build-arg VERSION=${DOCKER_TAG} .

# publish docker image to dockerhub
.PHONY: docker-publish
docker-publish:
	docker image push ${DOCKER_IMG}

# build docker image and publish to dopckerhub
.PHONY: dockerhub-update
dockerhub-update: docker-build docker-publish