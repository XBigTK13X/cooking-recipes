from jinja2 import Environment, FileSystemLoader

import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Environment(loader=FileSystemLoader(CURRENT_DIR))
TEMPLATE_DIR = os.path.join(CURRENT_DIR,'../template')
for root, dirs, files in os.walk(TEMPLATE_DIR):
	for file in files:
		print(file)
		#print templates.get_template('test_template.html').render(payload=payload)