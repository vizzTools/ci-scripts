
#!/bin/python3
# Run this to generate HTML docs suitable for jekyll gh-pages


# Remember to set environment variables in .env or CI config, e.g.;
#        DOCS_URL_PATH ="https://vizztools.github.io/vizzToolsCore"
#        SCHEMA_DIR_PATH="./json-schema"
#        JSONLD_DIR_PATH="./jsonld-examples"
#        DOCS_DIR_PATH="./docs"

import json
import os
import shutil
import sys

import yaml
from json_schema_for_humans.generate import (GenerationConfiguration,
                                             generate_from_filename)

# Set path when run in docs
sys.path.insert(0, os.path.abspath(".."))

# Define directory names of schema and examples
DOCS_URL_PATH = os.environ.get("DOCS_URL_PATH")
SCHEMA_DIR_PATH = os.environ.get("SCHEMA_DIR_PATH")
JSONLD_DIR_PATH = os.environ.get("JSONLD_DIR_PATH")
DOCS_DIR_PATH = os.environ.get("DOCS_DIR_PATH")

# Make directories in docs
DOCS_SCHEMA_PATH = os.path.join(os.getcwd(), DOCS_DIR_PATH, SCHEMA_DIR_PATH)
DOCS_JSONLD_PATH = os.path.join(os.getcwd(), DOCS_DIR_PATH, JSONLD_DIR_PATH)
DOCS_PATH = os.path.join(os.getcwd(), DOCS_DIR_PATH)
os.makedirs(DOCS_SCHEMA_PATH, exist_ok=True)
os.makedirs(DOCS_JSONLD_PATH, exist_ok=True)

# Add JSON-LD examples
print("\nProcessing JSON-LD")
for case_name in os.listdir(JSONLD_DIR_PATH):
    print(f"Processing {case_name}")
    name, ext = os.path.splitext(case_name)
    case_source = os.path.abspath(os.path.join(JSONLD_DIR_PATH, case_name))
    if os.path.isfile(case_source) and ext == ".jsonld":
        print(case_source)
        # replace @id with DOCS_URL_PATH + basename
        with open(case_source, "r") as f:
            obj = json.load(f)
            obj['$schema'] = os.path.join(DOCS_URL_PATH,os.path.basename(obj['$schema']))
            obj['@context'] = DOCS_URL_PATH
            print(obj['$schema'])
            print(obj['@context'])
            print("Writing to: ", os.path.join(DOCS_JSONLD_PATH, case_name), "\n")
        with open(os.path.join(DOCS_JSONLD_PATH, case_name), 'w') as f:
            json.dump(obj, f, indent=4, sort_keys=False)

# Convert Schema to HTML
print("\nProcessing JSON Schema")
out = []
fl = os.listdir(SCHEMA_DIR_PATH)
#pprint.pprint(fl)
for case_name in sorted(fl):
    print(f"Processing {case_name}")
    name, ext = os.path.splitext(case_name)
    name, _ = os.path.splitext(name)
    case_source = os.path.abspath(os.path.join(SCHEMA_DIR_PATH, case_name))
    if os.path.isfile(case_source) and ext == ".json":
        # replace @id with DOCS_URL_PATH + basename
        with open(case_source, "r") as f:
            obj = json.load(f)
            obj["$id"] = f"{DOCS_URL_PATH}/{SCHEMA_DIR_PATH}/{obj['$id']}"
            print("Updated $id: ", obj["$id"])
            print("Writing to index")
            yaml_data_dict = {'title': obj["title"], 'description': obj["description"]}
            out.append(yaml_data_dict)
            print("Writing to: ", os.path.join(DOCS_SCHEMA_PATH, case_name))
            with open(os.path.join(DOCS_SCHEMA_PATH, case_name), 'w') as f:
                json.dump(obj, f, indent=4, sort_keys=False)
        
            print(f"Generating example {name}")
            config = GenerationConfiguration(recursive_detection_depth=10000, expand_buttons=True, deprecated_from_description=True)
            generate_from_filename(
                os.path.join(SCHEMA_DIR_PATH, case_name),
                os.path.join(DOCS_PATH, f"{name}.html"),
                config=config
            )

# Write site index YAML
#pprint.pprint(out)        
with open(os.path.join(DOCS_PATH, "_data", "index.yml"),'w') as yamlfile:
    yaml.safe_dump(out, yamlfile)


