#!/usr/bin/env bash

if [[ -z "${VIRTUAL_ENV}" ]]; then
	echo "A virtualenv needs to be created and activated to run this script."
	exit 1
fi

echo "Setting up project..."

echo "Installing python dependencies..."
pip install -U pip
pip install -r requirements/dev.txt
pyenv rehash

echo "Linking postactivate and postdeactivate..."
ln -nsf "$(pwd)/bin/postactivate.sh" "${VIRTUAL_ENV}/bin/postactivate"
ln -nsf "$(pwd)/bin/postdeactivate.sh" "${VIRTUAL_ENV}/bin/postdeactivate"

echo "Installing npm dependencies..."
npm install

echo "Setting up pre-commit..."
pre-commit install
pre-commit

echo "Copying config.example.yml to config.yml..."
cp config.example.yml config.yml

echo "Project ready."
