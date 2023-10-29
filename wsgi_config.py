# arquivo para a configuração do WSGI
# normalmente encontrado em "/var/www"

import sys

# add your project directory to the sys.path
project_home = '/home/red2581/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application
