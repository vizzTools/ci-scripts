#!/bin/bash
# Convert JSON schema to Python classes.
set -ex

# Set the JSON schema source path(s)
# This should be of the form: 
#   {"<Type>": ["<schema-path>"], "<Type>": ["<schema-path>"]}
# where `Type` is the tope-level Type or Class name, and schema-path is a file or URL path.
# Note if using files, references ($ref) must be in same directory
# Note parsing only the top-level Type usually provides all sub Types.

#SCHEMA_SRC_PATHS="schema_src_paths.json" 

# Set the directory to add the generated Python code
# all Types will be added to a single file, Models.py
# and the __init__.py file updated to load all Types

#CODE_DIR=./vizzToolsCore

# TODO: add automatic semantic version
# TODO: automatically update __init__.py
#echo "from .Models import  *" | sudo tee -a $CODE_DIR/"__init__.py"

touch $CODE_DIR_PATH/Models.py

# Convert JSON schema to Python code
quicktype \
    --alphabetize-properties \
    --python-version 3.7 \
    --src-lang schema \
    --src-urls $SCHEMA_SRC_PATHS \
    -l py \
    -o $CODE_DIR_PATH/Models.py
echo "Code written to $CODE_DIR_PATH/Models.py"