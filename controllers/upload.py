import os
from flask import *
from werkzeug.utils import secure_filename

upload = Flask(__name__)

UPLOAD_FOLDER = '/vagrant/p3_o4fk7n/static/images'
upload.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER