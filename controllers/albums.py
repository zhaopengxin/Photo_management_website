from flask import *
from extensions import *
from upload import *
from main import db

albums = Blueprint('albums', __name__, template_folder='templates')


@albums.route('/m8pl2dh7/p3/albums')
def albums_route():
    holdername_to_check = request.args.get('username')
    if holdername_to_check == None:
        if 'username' in session: # has only username
            login = True
            sensitive = True
            holdername = session['username']
            username = session['username']
            album_list = query_albums_from_username(db, username)
        else: # has on holdername, no username
            return redirect(url_for('login.login_route'))
    else:
        holdername_list = check_username(db, holdername_to_check)
        if len(holdername_list) == 0: #holdername does not exist
            abort(404)
        else:
            holdername = holdername_list[0]['username']
        if 'username' in session: # has holdername and username      
            login = True
            username = session['username']
            if username == holdername:
                sensitive = True
            else:
                sensitive = False
            album_list = query_accessible_albums_from_username_holdername(db, username, holdername)
        else: #has only holdername
            login = False
            sensitive = False
            username = "annoymous"
            album_list = query_public_albums_from_holdername(db, holdername)
    options = {
        "login" : login,
        "edit" : False,
        "sensitive" : sensitive,
        "holdername" : holdername,
        "username" : username,
        "album_list" : album_list
    }
    return render_template("albums.html", **options)

@albums.route('/m8pl2dh7/p3/albums/edit', methods = ['GET', 'POST'])
def albums_edit_route():
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('login.login_route'))
     
    if request.method == 'POST':
        if request.form["op"] == "add":
            add_new_albums(db, username, request.form["title"])
        elif request.form["op"] == "delete":
            delete_old_albums(os, db, request.form["albumid"])
        else:
            abort(404)

    album_list = query_albums_from_username(db, username)
    options = {
        "login" : True,
        "edit": True,
        "sensitive" : True,
        "holdername": username,
        "username" : username,
        "album_list": album_list
        }
    return render_template("albums.html", **options)