from flask import *
from extensions import *
from main import db
import hashlib

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/m8pl2dh7/p3/api/v1/user', methods = ['GET', 'POST', 'PUT'])
def api_user_route():
    if request.method == 'GET':
        if 'username' in session:
            session_user = session['username']
            users = query_user_from_username(db, session_user)
            userDict = {
                'username' : users[0]['username'],
                'firstname': users[0]['firstname'],
                'lastname' : users[0]['lastname'],
                'email' : users[0]['email']
            }
            return jsonify(userDict)
        else:
            errors = [{"message" : "You do not have the necessary credentials for the resource"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 401

    if request.method == 'POST':
        user = request.get_json()
        required_fields = ['username', 'firstname', 'lastname', 'password1', 'password2', 'email']
        if check_empty_field(required_fields, user) == False:
            errors = [{"message" : "You do not provide the necessary fields"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 422
        else:
            username = user["username"]
            firstname = user["firstname"]
            lastname = user["lastname"]
            password1 = user["password1"]
            password2 = user["password2"]
            email = user["email"]

        # container for 422 error
        errors = []    
        if check_unique_username(db, username) == False:
            errors.append({"message" : "This username is taken"})
        if len(username) < 3:
            errors.append({"message" : "Usernames must be at least 3 characters long"})
        if check_content(username) == False:
            errors.append({"message" : "Usernames may only contain letters, digits, and underscores"})
        if len(password1) < 8:
            errors.append({"message" : "Passwords must be at least 8 characters long"})
        if check_password_element(password1) == False:
            errors.append({"message" : "Passwords must contain at least one letter and one number"})
        if check_content(password1) == False:
            errors.append({"message" : "Passwords may only contain letters, digits, and underscores"})
        if check_passwords_match(password1, password2) == False:
            errors.append({"message" : "Passwords do not match"})
        if check_email_format(email) == False:
            errors.append({"message" : "Email address must be valid"})
        if len(username) > 20:
            errors.append({"message" : "Username must be no longer than 20 characters"})
        if len(firstname) > 20:
            errors.append({"message" : "Firstname must be no longer than 20 characters"})
        if len(lastname) > 20:
            errors.append({"message" : "Lastname must be no longer than 20 characters"})
        if len(email) > 40:
            errors.append({"message" : "Email must be no longer than 40 characters"})

        if len(errors) > 0: # 422 error happens
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 422
        else: # valid input, so create user
            create_newuser_account(db, username, firstname, lastname, password1, email)
            userDict = {
                'username' : user['username'],
                'firstname': user['firstname'],
                'lastname' : user['lastname'],
                'email' : user['email']
            }
            return jsonify(userDict), 201

    if request.method == 'PUT':
        if 'username' in session:
            session_user = session['username']
            user = request.get_json()
            required_fields = ['username', 'firstname', 'lastname', 'password1', 'password2', 'email']
            if check_empty_field(required_fields, user) == False:
                errors = [{"message" : "You do not provide the necessary fields"}]
                errorDict = {
                    'errors' : errors
                }
                return jsonify(errorDict), 422
            else:
                username = user["username"]
                firstname = user["firstname"]
                lastname = user["lastname"]
                password1 = user["password1"]
                password2 = user["password2"]
                email = user["email"]

            if username != session_user:
                errors = [{"message" : "You do not have the necessary permissions for the resource"}]
                errorDict = {
                    'errors' : errors
                }
                return jsonify(errorDict), 403

        else:
            errors = [{"message" : "You do not have the necessary credentials for the resource"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 401            
           
        # container for 422 error
        errors = []    
        if check_content(username) == False:
            errors.append({"message" : "Usernames may only contain letters, digits, and underscores"})
        if password1 and check_password_min_len(password1) == False:
            errors.append({"message" : "Passwords must be at least 8 characters long"})
        if password1 and check_password_element(password1) == False:
            errors.append({"message" : "Passwords must contain at least one letter and one number"})
        if password1 and check_content(password1) == False:
            errors.append({"message" : "Passwords may only contain letters, digits, and underscores"})
        if password1 and check_passwords_match(password1, password2) == False:
            errors.append({"message" : "Passwords do not match"})
        if check_email_format(email) == False:
            errors.append({"message" : "Email address must be valid"})
        if len(firstname) > 20:
            errors.append({"message" : "Firstname must be no longer than 20 characters"})
        if len(lastname) > 20:
            errors.append({"message" : "Lastname must be no longer than 20 characters"})
        if len(email) > 40:
            errors.append({"message" : "Email must be no longer than 40 characters"})

        if len(errors) > 0: # 422 error happens
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 422
        else: # valid input, so create user
            update_user_account(db, username, 'firstname', firstname)
            update_user_account(db, username, 'lastname', lastname)
            update_user_account(db, username, 'email', email)
            if password1: # password1 is ""
                update_user_account(db, username, 'password', password1)

            userDict = {
                'username' : user['username'],
                'firstname': user['firstname'],
                'lastname' : user['lastname'],
                'email' : user['email']
            }
            return jsonify(userDict)

# /user[public]
@user.route('/m8pl2dh7/p3/user', methods = ['GET'])
def user_route():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('user.user_edit_route'))
        else:
            options = { "edit" : False }
            return render_template("user.html", **options)

# /user/edit[sensitve]
@user.route('/m8pl2dh7/p3/user/edit', methods = ['GET'])
def user_edit_route():
    if request.method == 'GET':
        if 'username' in session:
            options = { "edit" : True }
            return render_template("user.html", **options)
        else:
            return redirect(url_for('login.login_route') + "?url=" + url_for('user.user_edit_route'))


