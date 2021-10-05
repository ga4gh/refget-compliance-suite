DOCKER_ORG := ga4gh
DOCKER_REPO := refget-compliance-suite
DOCKER_TAG := $(shell cat setup.py | grep "version" | cut -f 2 -d '"')
DOCKER_IMG := ${DOCKER_ORG}/${DOCKER_REPO}:${DOCKER_TAG}
DOCKER_FILE := Dockerfile
DOCKER_REG_ADDR := registry.hub.docker.com
GIT_URL := git@github.com:yash-puligundla/refget-compliance-suite.git
GIT_REF := feature/add_wdl_cwl
CWL_PATH := /tools/cwl/refget_compliance_suite.cwl
WDL_PATH := /tools/wdl/refget_compliance_suite.wdl
CWL_TEST_PATH := /tools/cwl/refget_compliance_suite_config.cwl.json
WDL_TEST_PATH := /tools/wdl/refget_compliance_suite_config.wdl.json

# TO DO: 
# 1. test dockstore-add-version
# 2. change git_ref to use a release tag


# default
.PHONY: Nothing
Nothing:
	@echo "No target provided. Stop"

# build docker image
.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_IMG) --build-arg VERSION=${DOCKER_TAG} .

# publish docker image to dockerhub
.PHONY: docker-publish
docker-publish:
	docker image push ${DOCKER_IMG}

# build docker image and publish to dockerhub
.PHONY: dockerhub-update
dockerhub-update: docker-build docker-publish

# manual publish the tool to dockstore. 
# This command is used when the tool is published for the first time.
.PHONY: dockstore-manual-publish
dockstore-manual-publish:
	dockstore tool manual_publish --name ${DOCKER_REPO} --namespace ${DOCKER_ORG} --git-url ${GIT_URL} --git-reference ${GIT_REF} --version-name ${DOCKER_TAG} --dockerfile-path /${DOCKER_FILE}  --cwl-path ${CWL_PATH} --wdl-path ${WDL_PATH} --test-cwl-path ${CWL_TEST_PATH} --test-wdl-path ${WDL_TEST_PATH} --registry DOCKER_HUB
	dockstore tool test_parameter --entry ${DOCKER_REG_ADDR}/${DOCKER_ORG}/${DOCKER_REPO} --version ${DOCKER_TAG} --descriptor-type CWL --add ${CWL_TEST_PATH}
	dockstore tool test_parameter --entry ${DOCKER_REG_ADDR}/${DOCKER_ORG}/${DOCKER_REPO} --version ${DOCKER_TAG} --descriptor-type WDL --add ${WDL_TEST_PATH}

# add a new version to an existing dockstore tool.
.PHONY: dockstore-add-version
dockstore-add-version:
	dockstore tool version_tag add --entry ${DOCKER_REG_ADDR}/${DOCKER_ORG}/${DOCKER_REPO} --name ${DOCKER_TAG} --git-reference ${GIT_REF} --cwl-path ${CWL_PATH} --wdl-path ${WDL_PATH} --dockerfile-path /${DOCKER_FILE}
	dockstore tool test_parameter --entry ${DOCKER_REG_ADDR}/${DOCKER_ORG}/${DOCKER_REPO} --version ${DOCKER_TAG} --descriptor-type CWL --add ${CWL_TEST_PATH}
	dockstore tool test_parameter --entry ${DOCKER_REG_ADDR}/${DOCKER_ORG}/${DOCKER_REPO} --version ${DOCKER_TAG} --descriptor-type WDL --add ${WDL_TEST_PATH}