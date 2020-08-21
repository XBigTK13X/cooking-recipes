from jinja2 import Environment, FileSystemLoader

import shutil

import yaml

import os

TEMPLATE_DIR = 'template'
RECIPE_DIR = 'recipes'
SITE_ROOT = 'docs'

templateCache = {}
templates = Environment(loader=FileSystemLoader('template'))
# Preload all templates
for root, dirs, files in os.walk(TEMPLATE_DIR):
	for file in files:
		templateCache[file] = templates.get_template(file)


recipes = []
# Create a top-level directory of recipes for the index
for root, dirs, files in os.walk(RECIPE_DIR):
	for file in files:
		if file == "template.yaml":
			continue
		with open(os.path.join(root, file), 'r', encoding="utf8") as stream:
			recipe = yaml.load(stream, Loader=yaml.FullLoader)
			recipe['title'] = recipe['name'].title().replace("'S ", "'s ")
			recipe['slug'] = recipe['name'].replace(' ', '-')
			ingredients = recipe['ingredients']
			ingredients = sorted(ingredients, key=lambda k: k['name'])
			recipe['ingredients'] = ingredients
			if 'subrecipes' in recipe:
				for subrecipe in recipe['subrecipes']:
					subrecipe['title'] = subrecipe['name'].title().replace("'S ", "'s ")
					subrecipe['slug'] = subrecipe['name'].replace(' ', '-')
			recipes.append(recipe)

recipes = sorted(recipes, key=lambda k: k['slug'])

payload = {
	'recipes': recipes
}

landingHtml = templateCache['index.jinja'].render(payload=payload)

try:
	shutil.rmtree(SITE_ROOT)
except Exception as e:
	swallow = True

shutil.copytree('site', SITE_ROOT)

with open(SITE_ROOT+'/index.html', 'w') as stream:
	stream.write(landingHtml)
