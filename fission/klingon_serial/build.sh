#!/bin/bash
apk update
apk upgrade
apk add gcc python3-dev linux-headers musl-dev
pip3 install --prefer-binary -r ${SRC_PKG}/requirements.txt -t ${SRC_PKG} && cp -r ${SRC_PKG} ${DEPLOY_PKG}
