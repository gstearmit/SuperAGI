#!/bin/bash

# Downloads the tools
python chatdevagi/tool_manager.py

# Install dependencies
./install_tool_dependencies.sh

exec celery -A chatdevagi.worker worker --beat --loglevel=info