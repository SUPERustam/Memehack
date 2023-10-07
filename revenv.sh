#!/bin/bash

cp ~/turbo-broccoli/.gitignore .gitignore
pythonb -m venv .env
source .env/bin/activate
pip install --upgrade pip pylint autoflake isort 
pip install --upgrade pip setuptools pyright autopep8 pynvim debugpy neovim
pip install -r requirements.txt
cp ~/turbo-broccoli/.vimspector.json .vimspector.json
