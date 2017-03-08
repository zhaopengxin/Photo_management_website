from flask import *
import MySQLdb
from extensions import *

main = Blueprint('main', __name__, template_folder='templates')

db = connect_to_database()

@main.route('/m8pl2dh7/p3/')
def main_route():
    if 'username' in session:
        username = session['username']
        users= query_user_from_username(db, username)
        user = users[0]
        access_albums = query_accessible_albums_from_username(db, user["username"])
        options = {
            "access_albums": access_albums,
            "user" : user,   
            "login" : True
        }
    else:
        public_albums = query_public_albums(db)
        users = query_all_users(db)
        options = {
            "public_albums" : public_albums,
            "users" : users,
            "login" : False
        }
    return render_template("index.html", **options)
