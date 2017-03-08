import MySQLdb
import MySQLdb.cursors
import config
import re
import hashlib
import uuid

########## global variable ############
sequencenum = 30

########## general-use functions ############

def connect_to_database():
  options = {
    'host': config.env['host'],
    'user': config.env['user'],
    'passwd': config.env['password'],
    'db': config.env['db'],
    'cursorclass' : MySQLdb.cursors.DictCursor
  }
  db = MySQLdb.connect(**options)
  db.autocommit(True)
  return db

def check_empty_field(required_fields, user):
    for field in required_fields:
        if field not in user:
            return False
    return True

########## main.py (default homepage) ############

def query_public_albums(db):
    cur = db.cursor()
    command = 'SELECT albumid, title FROM Album WHERE access = "public"'
    cur.execute(command)
    public_albums = cur.fetchall()
    return public_albums

def query_all_users(db):
    cur = db.cursor()
    command = 'SELECT * FROM User'
    cur.execute(command)
    users = cur.fetchall()
    return users

########## main.py (logged in homepage) ############

def query_user_from_username(db, username):
    cur = db.cursor()
    command = 'SELECT * FROM User WHERE username = "' + username.lower() + '"'
    cur.execute(command)
    user = cur.fetchall()
    return user

def query_accessible_albums_from_username(db, username):
    cur = db.cursor()
    command1 = 'SELECT AB.albumid, AB.title FROM Album AB WHERE AB.username = "' + username.lower() + '"'
    command2 = ' UNION '
    command3 = 'SELECT AB.albumid, AB.title FROM Album AB, AlbumAccess AA, User U WHERE AB.albumid = AA.albumid AND U.username = AA.username AND U.username = "' + username.lower() +'"'
    command4 = ' UNION '
    command5 = 'SELECT AB.albumid, AB.title FROM Album AB WHERE AB.access = "public"'
    command = command1 + command2 + command3 + command4 + command5
    cur.execute(command)
    access_albums = cur.fetchall()
    return access_albums

########## user.py (new user page) ############

def create_newuser_account(db, username, firstname, lastname, password, email):
    cur = db.cursor()
    algorithm = "sha512"
    salt = uuid.uuid4().hex
    m = hashlib.new(algorithm)
    m.update(salt + password)
    password_hash = "$".join([algorithm, salt, m.hexdigest()])
    command1 = 'INSERT INTO User(username, firstname, lastname, password, email) VALUES'
    command2 = '("' + username.lower() + '","' + firstname + '","' + lastname + '","' + password_hash + '","' + email + '")'
    command = command1 + command2
    cur.execute(command)
    return

def update_user_account(db, username, fieldname, fieldvalue):
    if fieldname == "password":
        algorithm = "sha512"
        salt = uuid.uuid4().hex
        m = hashlib.new(algorithm)
        m.update(salt + fieldvalue)
        fieldvalue = "$".join([algorithm, salt, m.hexdigest()])

    cur = db.cursor()
    command = 'UPDATE User SET ' + fieldname + ' = "' + fieldvalue + '" WHERE username = "' + username.lower() + '"'
    cur.execute(command)
    return 

#-------------check_helper_functions------------------#
def check_unique_username(db, username):
    cur = db.cursor()
    command = 'SELECT username FROM User WHERE username = "' + username + '"'
    cur.execute(command)
    usernames = cur.fetchall()
    if len(usernames) == 0:
        return True
    else:
        return False

# can be used for username check and password check
def check_content(ss):
    u = list(ss)
    for i in xrange(0, len(ss)):
        if u[i] >= '0' and u[i] <= '9':
            continue
        elif u[i] >= 'a' and u[i] <= 'z':
            continue
        elif u[i] >= 'A' and u[i] <= 'Z':
            continue
        elif u[i] == '_':  
            continue
        else:
            return False
    return True

def check_password_element(password1):
    digit = False
    letter = False
    p = list(password1)
    for i in xrange(0, len(password1)):
        if p[i] >= '0' and p[i] <= '9':
            digit = True
        elif p[i] >= 'a' and p[i] <= 'z':
            letter = True
        elif p[i] >= 'A' and p[i] <= 'Z':
            letter = True
    return digit and letter

def check_passwords_match(password1, password2):
    return password1 == password2

def check_email_format(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    else:
        return True

########## login.py (user login page) ############

def check_username_existence(db, username):
    result = check_unique_username(db, username)
    if result:
        return False
    else:
        return True 

def check_password_correctness(db, username, password):
    cur = db.cursor()
    command = 'SELECT password FROM User WHERE username = "' + username.lower() + '"'
    cur.execute(command)
    password_str = cur.fetchall()[0]["password"]
    salt = password_str.split('$')[1]
    algorithm = "sha512"
    m = hashlib.new(algorithm)
    m.update(salt + password)
    password_hash = "$".join([algorithm, salt, m.hexdigest()])
    return password_hash == password_str

########## albums.py (albums page) ############

def query_albums_from_username(db, username):
    cur = db.cursor()
    command = 'SELECT albumid, title FROM Album WHERE username = "' + username.lower() + '"'
    cur.execute(command)
    albums = cur.fetchall()
    return albums

def query_accessible_albums_from_username_holdername(db, username, holdername):
    cur = db.cursor()
    if username == holdername:
        return query_albums_from_username(db, username)
    else:
        command1 = 'SELECT AB.albumid, AB.title FROM Album AB, AlbumAccess AA WHERE '
        command2 = 'AB.albumid = AA.albumid AND AB.username = "' + holdername + '" AND AA.username = "' + username.lower() + '"' 
        command3 = ' UNION '
        command4 = 'SELECT AB.albumid, AB.title FROM Album AB WHERE AB.access = "public" AND AB.username = "' + holdername + '"'
        command = command1 + command2 + command3 + command4
        cur.execute(command)
        albums = cur.fetchall()
        return albums 

def query_public_albums_from_holdername(db, holdername):
    cur = db.cursor()
    command = 'SELECT albumid, title FROM Album WHERE username = "' + holdername + '" AND access = "public"'
    cur.execute(command)
    albums = cur.fetchall()
    return albums


def add_new_albums(db, username, title):
    cur = db.cursor()
    command = 'INSERT INTO Album(title, username, access) VALUES ("' + title + '","' + username.lower() + '", "private")'
    cur.execute(command)
    return

def delete_old_albums(os, db, albumid):
    cur = db.cursor()
    command1 = 'SELECT picid FROM Contain WHERE albumid = "' + albumid + '"'
    cur.execute(command1)
    picids = cur.fetchall()
    for picid in picids:
        delete_from_image_folder(os, db, picid["picid"])
    command2 = 'DELETE FROM Album WHERE albumid = "' + albumid + '"'
    cur.execute(command2)
    return

########## album.py (album page) ############

def check_album_sensitive(db, username, albumid):
    cur = db.cursor()
    if username == None:
        return False
    command = 'SELECT AB.albumid FROM Album AB WHERE AB.username = "' + username.lower() + '" AND AB.albumid = "' + str(albumid) + '"'
    cur.execute(command)
    albumids = cur.fetchall()
    if len(albumids) == 1:
        return True
    else:
        return False

def query_pic_from_albumid(db, albumid):
    cur = db.cursor()
    command = 'SELECT C.picid, C.caption, C.albumid, C.sequencenum, P.format, P.date  FROM Contain C INNER JOIN Photo P ON C.picid = P.picid WHERE C.albumid = "' + str(albumid) + '"'
    cur.execute(command)
    pic_infos = cur.fetchall()
    return pic_infos

def query_album_from_albumid(db, albumid):
    cur = db.cursor()
    command = "SELECT * FROM Album WHERE albumid = '" + str(albumid) + "'"
    cur.execute(command)
    album_infos = cur.fetchall()[0]
    return album_infos

def check_album_existence(db, albumid):
    cur = db.cursor()
    command = "SELECT * FROM Album WHERE albumid = '" + str(albumid) + "'"
    cur.execute(command)
    album_infos = cur.fetchall()
    return len(album_infos) == 1

########## album.py (album edit page) ############

def change_album_access(db, albumid, access):
    cur = db.cursor()
    command1 = 'SELECT access FROM Album WHERE albumid = "' + str(albumid) + '"'
    cur.execute(command1)
    old_access = cur.fetchall()[0]
    if old_access == access:
        return
    else:
        change_lastupdated(db, albumid)
        command2 = 'UPDATE Album SET access = "' + access + '" WHERE albumid = "' + str(albumid) + '"'
        cur.execute(command2)
        if access == "public":
            command3 = 'DELETE FROM AlbumAccess WHERE albumid = "' + str(albumid) + '"'
            cur.execute(command3)
        return

def revoke_user_access_to_album(db, username, albumid):
    cur = db.cursor()
    command = 'DELETE FROM AlbumAccess WHERE username = "' + username.lower() + '" AND albumid = "' + str(albumid) + '"'
    cur.execute(command)
    return

def grant_user_access_to_album(db, username, albumid):
    cur = db.cursor()
    command = 'INSERT INTO AlbumAccess(albumid, username) VALUES ("' + str(albumid) + '", "' + username.lower() + '")'
    cur.execute(command)
    return

def query_access_users_from_albumid(db, albumid):
    cur = db.cursor()
    command = 'SELECT username FROM AlbumAccess WHERE albumid = "' + str(albumid) + '"'
    cur.execute(command)
    access_users = cur.fetchall()
    return access_users

def add_pic_into_album(db, albumid, picid, filename):
    cur=db.cursor()
    command="INSERT INTO Photo(picid, format) VALUES ('" + picid + "','" + filename.rsplit('.', 1)[-1] + "')"
    cur.execute(command)
    return

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'bmp'])
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

def add_pic_into_Contain(db, albumid, picid):
    global sequencenum
    cur=db.cursor()  
    command="INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (" + str(sequencenum) + ",'" + str(albumid) +"','"+picid+"','')"
    cur.execute(command)
    sequencenum += 1;
    return

def delete_from_image_folder(os, db, picid):
    cur = db.cursor() 

    command1 = "SELECT format FROM Photo WHERE picid = '" + picid + "'"
    cur.execute(command1)
    formats = cur.fetchall()
    postfix = formats[0]["format"]
    
    command2 = "DELETE FROM Photo WHERE picid = '" + picid + "'"
    cur.execute(command2)
    delete_from_os_command = "/vagrant/p3_o4fk7n/static/images/" + picid + "." + postfix

    os.remove(delete_from_os_command)
    return   

def check_username(db, username_to_check):
    cur = db.cursor()
    command = "SELECT username FROM User WHERE username = '" + username_to_check.lower() + "'"
    cur.execute(command)
    username_list = cur.fetchall()
    return username_list

def check_albumid(db, albumid_to_check):
    cur = db.cursor()
    command = "SELECT albumid FROM Album WHERE albumid = '" + albumid_to_check + "'"
    cur.execute(command)
    albumid_list = cur.fetchall()
    return albumid_list

########## pic.py (view picture page) ############
def update_caption(db, albumid, picid, caption):
    cur = db.cursor()
    command1 = 'SELECT C.caption FROM Contain C WHERE C.picid = "' + picid + '"'
    cur.execute(command1)
    old_caption = cur.fetchall()[0]
    if old_caption == caption:
        return
    else:
        change_lastupdated(db, albumid)
        command2 = 'UPDATE Contain SET caption = "' + caption + '" WHERE picid = "' + picid + '"'
        cur.execute(command2)
        return

def get_previous_pic(db, picid):
    cur = db.cursor()
    command1 = "SELECT albumid, sequencenum FROM Contain WHERE picid = '" + picid  + "'"
    cur.execute(command1)
    infos = cur.fetchall()
    albumid = infos[0]["albumid"]
    sequencenum = infos[0]["sequencenum"]
    command2 = "SELECT picid FROM Contain WHERE albumid = '" + str(albumid) + "' AND sequencenum < '" + str(sequencenum) + "'" 
    cur.execute(command2)
    candidates = cur.fetchall();
    prev_picid = None
    if(candidates): #if array is not empty
        prev_picid = candidates[-1]["picid"]
    return prev_picid

def get_next_pic(db, picid):
    cur = db.cursor()
    command1 = "SELECT albumid, sequencenum FROM Contain WHERE picid = '" + picid  + "'"
    cur.execute(command1)
    infos = cur.fetchall()
    albumid = infos[0]["albumid"]
    sequencenum = infos[0]["sequencenum"]
    command2 = "SELECT picid FROM Contain WHERE albumid = '" + str(albumid) + "' AND sequencenum > '" + str(sequencenum) + "'" 
    cur.execute(command2)
    candidates = cur.fetchall();
    next_picid = None
    if(candidates): #if array is not empty
        next_picid = candidates[0]["picid"]
    return next_picid

def query_pic_from_picid(db, picid):
    cur = db.cursor()
    command = "SELECT P.picid, C.caption, P.format, C.albumid FROM Photo P, Contain C WHERE P.picid = '" + picid + "' AND P.picid = C.picid"
    cur.execute(command)
    pic = cur.fetchall()[0]
    return pic 

def check_picture_existence(db, picid):
    cur = db.cursor()
    command = "SELECT * FROM Photo WHERE picid = '" + picid + "'"
    cur.execute(command)
    pic_infos = cur.fetchall()
    return len(pic_infos) == 1

def change_lastupdated(db, albumid):
    cur = db.cursor()
    command = "UPDATE  Album SET lastupdated = NOW() WHERE albumid = '" + str(albumid) + "'"
    cur.execute(command)
    return

def get_album_accessibility(db, albumid):
    cur = db.cursor()
    command = 'SELECT AB.access FROM Album AB WHERE AB.albumid = "' + str(albumid) + '"'
    cur.execute(command)
    access = cur.fetchall()[0]['access']
    return access














#####################   ACHIVE CODE    ####################

########## user.py (new user page) ############
"""
def check_blank_field_user(username, firstname, lastname, password1, email):
    result = []
    if len(username) == 0:
        result.append("Username")
    if len(firstname) == 0:
        result.append("Firstname")
    if len(lastname) == 0:
        result.append("Lastname")
    if len(password1) == 0:
        result.append("Password1")
    if len(email) == 0:
        result.append("Email")
    return result

def check_name_max_len(username, firstname, lastname):
    result = []
    if len(username) > 20:
        result.append("Username")
    if len(firstname) > 20:
        result.append("Firstname")
    if len(lastname) > 20:
        result.append("Lastname")
    return result

def check_username_min_len(username):
    if len(username) < 3:
        return False
    else:
        return True

def check_email_max_len(email):
    if len(email) > 40:
        return False
    else:
        return True

def check_password_min_len(password1):
    if len(password1) < 8:
        return False
    else:
        return True
"""

########## login.py (user login page) ############
"""
def check_blank_field_login(username, password):
    result = []
    if len(username) == 0:
        result.append("Username")
    if len(password) == 0:
        result.append("Password")
    return result
"""

########## album.py (album page) ############
"""
def check_album_accessibility(db, username, albumid):
    cur = db.cursor()
    if username == None:
        command = 'SELECT AB.albumid FROM Album AB WHERE AB.access = "public" AND AB.albumid = "' + str(albumid) + '"'
    else:
        command1 = 'SELECT AB.albumid FROM Album AB WHERE AB.access = "public" AND AB.albumid = "' + str(albumid) + '"'
        command2 = ' UNION '
        command3 = 'SELECT AB.albumid FROM Album AB WHERE AB.username = "' + username.lower() + '" AND AB.albumid = "' + str(albumid) + '"'
        command4 = ' UNION '
        command5 = 'SELECT AA.albumid FROM AlbumAccess AA WHERE AA.username = "' + username.lower() + '" AND AA.albumid = "' + str(albumid) + '"'
        command = command1 + command2 + command3 + command4 + command5
    cur.execute(command)
    albumids = cur.fetchall()
    if len(albumids) == 1:
        return True
    else:
        return False
"""

########## pic.py (view picture page) ############
"""
def query_albumid_from_picid(db, picid):
    cur = db.cursor()
    command1 = "SELECT albumid FROM Contain WHERE picid = '" + picid  + "'"
    cur.execute(command1)
    infos = cur.fetchall()
    albumid = infos[0]["albumid"]
    return albumid

def check_picid(db, picid_to_check):
    cur = db.cursor()
    command = "SELECT picid FROM Photo WHERE picid = '" + picid_to_check + "'"
    cur.execute(command)
    picid_list = cur.fetchall()
    return picid_list
"""

