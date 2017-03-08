from flask import *
from extensions import *
from main import db

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/m8pl2dh7/p3/api/v1/pic/<picid>', methods = ['GET','PUT'])
def api_pic_route(picid):
    if request.method == 'GET':
        if check_picture_existence(db, picid) == False:
            errors = [{"message" : "The requested resource could not be found"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 404
        else:
            pic = query_pic_from_picid(db, picid)
            picid_prev = get_previous_pic(db, picid)
            picid_next = get_next_pic(db, picid)
            albumid = pic['albumid']
            access = get_album_accessibility(db, albumid)
            username = query_album_from_albumid(db, albumid)['username']

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

        picDict = {
            'albumid' : pic['albumid'],
            'caption' : pic['caption'],
            'format' : pic['format'],
            'picid' : pic['picid'],
            'next' : picid_next,
            'prev' : picid_prev           
        }
        return jsonify(picDict)

    if request.method == 'PUT':
        pic = request.get_json()
        print(pic)
        required_fields = ['albumid', 'caption', 'format', 'next', 'picid', 'prev']
        if check_empty_field(required_fields, pic) == False:
            errors = [{"message" : "You do not provide the necessary fields"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 422
        else:
            albumid_new = pic['albumid']
            caption_new = pic['caption']
            format_new = pic['format']
            next_new = pic['next']
            picid_new = pic['picid']
            prev_new = pic['prev']

        if check_picture_existence(db, picid) == False:
            errors = [{"message" : "The requested resource could not be found"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 404
        else:
            pic_old = query_pic_from_picid(db, picid)
            albumid_old = pic_old['albumid']
            caption_old = pic_old['caption']
            format_old = pic_old['format']
            prev_old = get_previous_pic(db, picid)
            picid_old = pic_old['picid']
            next_old = get_next_pic(db, picid)
            access = get_album_accessibility(db, albumid_old)
            username = query_album_from_albumid(db, albumid_old)['username']

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

        if (albumid_new != albumid_old) or (format_new != format_old) or (next_new != next_old) or (picid_new != picid_old) or (prev_new != prev_old):
            errors = [{"message" : "You can only update caption"}]
            errorDict = {
                'errors' : errors
            }
            return jsonify(errorDict), 403  

        update_caption(db, albumid_new, picid, pic['caption'])
        return jsonify(pic), 200



@pic.route('/m8pl2dh7/p3/pic', methods = ['GET'])
def pic_route():
    options = {
        "edit" : False
    }
    return render_template("album.html", **options);
    

