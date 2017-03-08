from flask import *
from extensions import *
from main import db

logout = Blueprint('logout', __name__, template_folder='templates')

@logout.route('/m8pl2dh7/p3/api/v1/logout', methods = ['POST'])
def api_logout_route():
    if request.method == 'POST':
        if 'username' in session:
            session.pop('username', None)
            return jsonify(), 204
        else:
            errors = [{"message" : "You do not have the necessary credentials for the resource"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 401

@logout.route('/m8pl2dh7/p3/logout', methods = ['GET'])
def logout_route():
    return render_template("base.html")
