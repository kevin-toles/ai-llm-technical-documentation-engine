#!/bin/zsh
# Double-click this file to launch the Desktop App

cd "$(dirname "$0")"
PYTHONPATH=. python3 ui/desktop_app.py
