from jinja2 import Environment, FileSystemLoader

import yaml

import os

TEMPLATE_DIR = 'template'
RECIPE_DIR = 'input'

templateCache = {}
templates = Environment(loader=FileSystemLoader('template'))
# Preload all templates
for root, dirs, files in os.walk(TEMPLATE_DIR):
	for file in files:		
		templateCache[file] = templates.get_template(file)

payload = {
	'recipes':[]
}

# Create a top-level directory of recipes for the index
for root, dirs, files in os.walk(RECIPE_DIR):
	for file in files:
		with open(os.path.join(root,file), 'r') as stream:
			recipe = yaml.load(stream)
			payload['recipes'].append(recipe)

import pprint
pprint.pprint(payload)

print(templateCache['index.jinja'].render(payload=payload))