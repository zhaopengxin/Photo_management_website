from flask import *
from extensions import *
from main import db
from upload import *
import hashlib

album = Blueprint('album', __name__, template_folder='templates')

@album.route('/m8pl2dh7/p3/api/v1/album/<albumid>', methods = ['GET'])
def api_album_route(albumid):
    if check_album_existence(db, albumid) == False:
        errors = [{"message" : "The requested resource could not be found"}]
        errorDict = {
            'errors' : errors
        }
        return jsonify(errorDict), 404
    else:
        pic_infos = query_pic_from_albumid(db, albumid)
        album = query_album_from_albumid(db, albumid)
        access = album['access']
        username = album['username']
        pics = []
        for pic in pic_infos:
            item = {
                'albumid' : pic['albumid'],
                'caption' : pic['caption'],
                'date' : pic['date'],
                'format' : pic['format'],
                'picid' : pic['picid'],
                'sequencenum': pic['sequencenum']
            }
            pics.append(item)

    if access == 'private':
        if 'username' in session:
            session_user = session['username']
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

    albumDict = {
        'access' : album['access'],
        'albumid' : album['albumid'],
        'created' : album['created'],
        'lastupdated' : album['lastupdated'],
        'pics' : pics,
        'title' : album['title'],
        'username' : album['username']
    }
    return jsonify(albumDict)


@album.route('/m8pl2dh7/p3/album', methods = ['GET'])
def album_route():
    options = {
        "edit" : False
    }
    return render_template("album.html", **options);











#no change should be made to album_edit_route in P3
@album.route('/m8pl2dh7/p3/album/edit', methods = ['GET','POST'])
def album_edit_route():
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('login.login_route'))

    albumid_to_check = request.args.get('albumid')
    if albumid_to_check == None:
        abort(404)
    albumid_list = check_albumid(db, albumid_to_check)
    if len(albumid_list) == 0:
        abort(404)
    albumid = albumid_list[0]["albumid"]

    sensitive = check_album_sensitive(db, username, albumid)

    if sensitive == False: # user is not authorized to edit album
        abort(403)

    if request.method == 'POST':
        if request.form["op"] == "add":
            file = request.files['file']
            if file and allowed_file(file.filename):
                change_lastupdated(db, albumid)
                filename = secure_filename(file.filename)
                m = hashlib.md5(str(albumid)+filename)
                picid = m.hexdigest()
                file.save(os.path.join(upload.config['UPLOAD_FOLDER'], picid + "." + filename.rsplit('.',1)[-1]))
                add_pic_into_album(db, albumid, picid, filename)
                add_pic_into_Contain(db, albumid, picid)
        elif request.form["op"] == "delete":
            change_lastupdated(db, albumid)
            picid = request.form["picid"]
            delete_from_image_folder(os, db, picid)
        elif request.form["op"] == "access":
            access = request.form["access"]
            change_album_access(db, albumid, access)
        elif request.form["op"] == "revoke":
            user_revoke = request.form["username"]
            revoke_user_access_to_album(db, user_revoke, albumid)
        elif request.form["op"] == "grant":
            user_grant_to_check = request.form["username"]
            user_grant_list = check_username(db, user_grant_to_check)
            if len(user_grant_list) == 0:
                abort(404)
            else:
                user_grant = user_grant_list[0]["username"]
                if user_grant != username:
                    grant_user_access_to_album(db, user_grant, albumid)
        else:
            abort(404)

    pic_infos = query_pic_from_albumid(db, albumid)
    album = query_album_from_albumid(db, albumid)
    access_users = query_access_users_from_albumid(db, albumid)
    if album['access'] == "private":
        private = True
    else:
        private = False
    options = {
        "login" : True,
        "edit" : True,
        "sensitive" : True,
        "albumid" : albumid,
        "pic_infos" : pic_infos,
        "album" : album,
        "private" : private,
        "access_users" : access_users
    }
    return render_template("album.html", **options)

