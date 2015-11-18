#!/bin/bash

if [ -d ".env" ]; then
	mv requirements.txt requirements.txt.old
	./.env/bin/pip freeze > requirements.txt
	rm -rf .env
fi

virtualenv .env
./.env/bin/pip install -r requirements.txt

