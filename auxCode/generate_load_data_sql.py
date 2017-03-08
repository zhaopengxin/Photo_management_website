import hashlib
import uuid

filenames = ['football_s1.jpg', 'football_s2.jpg', 'football_s3.jpg', 'football_s4.jpg',
            'space_EagleNebula.jpg', 'space_GalaxyCollision.jpg', 'space_HelixNebula.jpg', 'space_MilkyWay.jpg',
            'space_OrionNebula.jpg', 'sports_s1.jpg', 'sports_s2.jpg', 'sports_s3.jpg',
            'sports_s4.jpg', 'sports_s5.jpg', 'sports_s6.jpg', 'sports_s7.jpg', 
            'sports_s8.jpg', 'world_EiffelTower.jpg', 'world_firenze.jpg', 'world_GreatWall.jpg', 
            'world_Isfahan.jpg', 'world_Istanbul.jpg', 'world_Persepolis.jpg', 'world_Reykjavik.jpg',
            'world_Seoul.jpg', 'world_Stonehenge.jpg', 'world_TajMahal.jpg', 'world_TelAviv.jpg',
            'world_tokyo.jpg', 'world_WashingtonDC.jpg'
]

# generate hashed picids
picids = []
for x in xrange(1,5):
    m = hashlib.md5(str(2) + filenames[x-1])
    picids.append(m.hexdigest())
for x in xrange(5,10):
    m = hashlib.md5(str(4) + filenames[x-1])
    picids.append(m.hexdigest())
for x in xrange(10,18):
    m = hashlib.md5(str(1) + filenames[x-1])
    picids.append(m.hexdigest())
for x in xrange(18,31):
    m = hashlib.md5(str(3) + filenames[x-1])
    picids.append(m.hexdigest())

# generate hashed password with salt
algorithm  = "sha512"
passwords = ["paulpass93", "rebeccapass15", "bob1pass"]
passwords_hash = []

for x in xrange(0,3):
    salt = uuid.uuid4().hex
    m = hashlib.new(algorithm)
    m.update(salt + passwords[x])
    password_hash = m.hexdigest()
    passwords_hash.append("$".join([algorithm, salt, password_hash]))

# populate the printing result
print_str = ''
print_str += 'INSERT INTO User(username, firstname, lastname, password, email)\n' 
print_str += '    VALUES\n'
print_str += '    ("sportslover", "Paul", "Walker","' + passwords_hash[0] + '","sportslover@hotmail.com"),\n' 
print_str += '    ("traveler", "Rebecca", "Travolta","' + passwords_hash[1] + '","rebt@explorer.org"),\n'
print_str += '    ("spacejunkie", "Bob", "Spacey","' + passwords_hash[2] + '","bspace@spacejunkie.net");\n\n\n'


print_str += 'INSERT INTO Album(title, username, access)\n'
print_str += '    VALUES\n'
print_str += '    ("I love sports", "sportslover", "public"),\n'
print_str += '    ("I love football", "sportslover", "private"),\n'
print_str += '    ("Around The World", "traveler", "public"),\n'
print_str += '    ("Cool Space Shots", "spacejunkie", "private");\n\n\n'

print_str += 'INSERT INTO Photo(picid, format)\n'
print_str += '    VALUES\n'

for x in xrange(1,30):
    print_str += '    ("' + picids[x-1] + '", "jpg"),\n'
print_str += '    ("' + picids[29] + '", "jpg");\n\n\n'

print_str += 'INSERT INTO Contain(sequencenum, albumid, picid, caption)\n'
print_str += '    VALUES\n'
count = 0
for x in xrange(0,4):
    print_str += '    (' + str(count) + ',2, "' + picids[x] +'",""),\n'
    count += 1
for x in xrange(4,9): 
    print_str += '    (' + str(count) + ',4, "' + picids[x] +'",""),\n'
    count += 1
for x in xrange(9,17):
    print_str += '    (' + str(count) + ',1, "' + picids[x] +'",""),\n'
    count += 1
for x in xrange(17,29):
    print_str += '    (' + str(count) + ',3, "' + picids[x] +'",""),\n'
    count += 1
print_str += '    (' + str(count) + ',3, "' + picids[29] +'","");\n\n\n'

print (print_str)