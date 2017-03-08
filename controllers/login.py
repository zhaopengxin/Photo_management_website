from flask import *
from extensions import *
from main import db
import hashlib

login = Blueprint('login', __name__, template_folder='templates')

@login.route('/m8pl2dh7/p3/api/v1/login', methods = ['POST'])
def api_login_route():
    if request.method == 'POST':
        user = request.get_json()
        required_fields = ['username', 'password']
        if check_empty_field(required_fields, user) == False:
            errors = [{"message" : "You do not provide the necessary fields"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 422
        else:
            username = user['username']
            password = user['password']

        if check_username_existence(db, username) == False:
            errors = [{"message" : "Username does not exist"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 404

        if check_password_correctness(db, username, password) == False:
            errors = [{"message" : "Password is incorrect for the specified username"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 422

        #create a new session for logging in
        session['username']= user['username'];

        userDict = {
            'username' : user['username']
        }

        return jsonify(userDict)


@login.route('/m8pl2dh7/p3/login', methods = ['GET'])
def login_route():
    if request.method == 'GET':
        return render_template("login.html")


