CREATE TABLE User(
    username VARCHAR(20), 
    firstname VARCHAR(20), 
    lastname VARCHAR(20), 
    password VARCHAR(256), 
    email VARCHAR(40),
    PRIMARY KEY(username)
);

CREATE TABLE Album(
    albumid INT AUTO_INCREMENT,
    title VARCHAR(50),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(20),
    access ENUM('public','private'),    
    PRIMARY KEY(albumid),
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE
);

CREATE TABLE Photo(
    picid VARCHAR(40),
    format VARCHAR(3),
    date TIMESTAMP,
    PRIMARY KEY(picid)
);

CREATE TABLE Contain(
    sequencenum INT, /* not? auto incrementing, value will start at 0*/
    albumid INT,
    picid VARCHAR(40),
    caption VARCHAR(255),
    PRIMARY KEY(sequencenum),
    FOREIGN KEY (albumid) REFERENCES Album(albumid) ON DELETE CASCADE,
    FOREIGN KEY (picid) REFERENCES Photo(picid) ON DELETE CASCADE
);


CREATE TABLE AlbumAccess(
    albumid INT,
    username VARCHAR(20),
    PRIMARY KEY (albumid, username),
    FOREIGN KEY (albumid) REFERENCES Album(albumid) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE
);
