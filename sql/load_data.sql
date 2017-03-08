INSERT INTO User(username, firstname, lastname, password, email)
    VALUES
    ("sportslover", "Paul", "Walker","sha512$56bd2ae441e047e69254659a6f3b467d$4fc29da5b18d13d807ac7353a9aedf707814755291c9de0620948d8cf383c8bf51a1fd09eb3907cbba446ab256179e5e0d97b202d21a44b05655a6c462c7d037","sportslover@hotmail.com"),
    ("traveler", "Rebecca", "Travolta","sha512$732cca2d1e6f4e02b7e0db3d72dcaa96$165ee544b7a39404d9d74576b8f577a5276d4052e5f271787e2087bc5b520711f3deab8eccab93bb0411669f8b972f1a08d045863eb95a7b21b7eb7a1a77919b","rebt@explorer.org"),
    ("spacejunkie", "Bob", "Spacey","sha512$9d3003c30a5547edbff37306a5572c86$e12a356355e68f26a305393be46d3bcd627cd5fb025c78e031e9460a4cc1b5a232a0350715cf4f94bc4cd2f9cb175c64828fcff0970b3b472523816df17c773e","bspace@spacejunkie.net");


INSERT INTO Album(title, username, access)
    VALUES
    ("I love sports", "sportslover", "public"),
    ("I love football", "sportslover", "private"),
    ("Around The World", "traveler", "public"),
    ("Cool Space Shots", "spacejunkie", "private");


INSERT INTO Photo(picid, format)
    VALUES
    ("001025dd643b0eb0661e359de86e3ea9", "jpg"),
    ("9a0a7d25af4f7a73f67dde74e8e54cff", "jpg"),
    ("c8e60100f13ffe374d59e39dc4b6a318", "jpg"),
    ("5e8b6207f007338243d3e29d6b82acab", "jpg"),
    ("4ddba6e2f905e9778c6b6a48b6fc8e03", "jpg"),
    ("09d8a979fa638125b02ae1578eb943fa", "jpg"),
    ("143ba34cb5c7e8f12420be1b576bda1a", "jpg"),
    ("e615a10fc4222ede59ca3316c3fb751c", "jpg"),
    ("65fb1e2aa4977d9414d1b3a7e4a3badd", "jpg"),
    ("b94f256c23dec8a2c0da546849058d9e", "jpg"),
    ("01e37cbdd55913df563f527860b364e8", "jpg"),
    ("8d554cd1d8bb7b49ca798381d1fc171b", "jpg"),
    ("2e9e69e19342b98141789925e5f87f60", "jpg"),
    ("298e8943ef1942159ef88be21c4619c9", "jpg"),
    ("cefe45eaeaeb599256dda325c2e972da", "jpg"),
    ("bf755d13bb78e1deb59ef66b6d5c6a70", "jpg"),
    ("5f8d7957874f1303d8300e50f17e46d6", "jpg"),
    ("bac4fca50bed35b9a5646f632bf4c2e8", "jpg"),
    ("f5b57bd7a2c962c54d55b5ddece37158", "jpg"),
    ("b7d833dd3aae203ca618759fc6f4fc01", "jpg"),
    ("faa20c04097d40cb10793a19246f2754", "jpg"),
    ("aaaadd578c78d21defaa73e7d1f08235", "jpg"),
    ("adb5c3af19664129141268feda90a275", "jpg"),
    ("abf97ffd1f964f42790fb358e5258e8d", "jpg"),
    ("ea2db8b970671856e43dd011d7df5fad", "jpg"),
    ("76d79b81b9073a2323f0790965b00a68", "jpg"),
    ("6510a4add59ef655ae3f0b6cdb24e140", "jpg"),
    ("28d38afca913a728b2a6bcf01aa011cd", "jpg"),
    ("5fb04eb11cbf99429a05c12ce2f50615", "jpg"),
    ("39ee267d13ccd32b50c1de7c2ece54d6", "jpg");


INSERT INTO Contain(sequencenum, albumid, picid, caption)
    VALUES
    (0,2, "001025dd643b0eb0661e359de86e3ea9",""),
    (1,2, "9a0a7d25af4f7a73f67dde74e8e54cff",""),
    (2,2, "c8e60100f13ffe374d59e39dc4b6a318",""),
    (3,2, "5e8b6207f007338243d3e29d6b82acab",""),
    (4,4, "4ddba6e2f905e9778c6b6a48b6fc8e03",""),
    (5,4, "09d8a979fa638125b02ae1578eb943fa",""),
    (6,4, "143ba34cb5c7e8f12420be1b576bda1a",""),
    (7,4, "e615a10fc4222ede59ca3316c3fb751c",""),
    (8,4, "65fb1e2aa4977d9414d1b3a7e4a3badd",""),
    (9,1, "b94f256c23dec8a2c0da546849058d9e",""),
    (10,1, "01e37cbdd55913df563f527860b364e8",""),
    (11,1, "8d554cd1d8bb7b49ca798381d1fc171b",""),
    (12,1, "2e9e69e19342b98141789925e5f87f60",""),
    (13,1, "298e8943ef1942159ef88be21c4619c9",""),
    (14,1, "cefe45eaeaeb599256dda325c2e972da",""),
    (15,1, "bf755d13bb78e1deb59ef66b6d5c6a70",""),
    (16,1, "5f8d7957874f1303d8300e50f17e46d6",""),
    (17,3, "bac4fca50bed35b9a5646f632bf4c2e8",""),
    (18,3, "f5b57bd7a2c962c54d55b5ddece37158",""),
    (19,3, "b7d833dd3aae203ca618759fc6f4fc01",""),
    (20,3, "faa20c04097d40cb10793a19246f2754",""),
    (21,3, "aaaadd578c78d21defaa73e7d1f08235",""),
    (22,3, "adb5c3af19664129141268feda90a275",""),
    (23,3, "abf97ffd1f964f42790fb358e5258e8d",""),
    (24,3, "ea2db8b970671856e43dd011d7df5fad",""),
    (25,3, "76d79b81b9073a2323f0790965b00a68",""),
    (26,3, "6510a4add59ef655ae3f0b6cdb24e140",""),
    (27,3, "28d38afca913a728b2a6bcf01aa011cd",""),
    (28,3, "5fb04eb11cbf99429a05c12ce2f50615",""),
    (29,3, "39ee267d13ccd32b50c1de7c2ece54d6","");



