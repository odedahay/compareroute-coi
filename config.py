import os
import jinja2

# Define root directory as this file location
ROOT_DIR = os.path.dirname(__file__)

# Add templates directory into jinja environment
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
JINJA_ENV = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATES_DIR),
                               autoescape = True)