import datetime
import bcrypt
import pymysql
import generators as gen

connection = None

def connect():
    global connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1204', 
        autocommit=True
    )

def disconnect():
    global connection
    connection.close()

def initialize():
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS qwicclick")
    cursor.execute("USE qwicclick")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        userid VARCHAR(64) PRIMARY KEY,
        username VARCHAR(64) NOT NULL UNIQUE,
        password VARCHAR(128) NOT NULL,
        email VARCHAR(64) NOT NULL UNIQUE,
        preference VARCHAR(10) DEFAULT FALSE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Links (
        userid VARCHAR(64),
        linkid VARCHAR(64) PRIMARY KEY,
        shortlink VARCHAR(64) NOT NULL UNIQUE,
        longlink TEXT NOT NULL,
        fingerprint BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (userid) REFERENCES Users(userid)
            ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sessions (
        sessiontoken VARCHAR(64) PRIMARY KEY,
        userid VARCHAR(64),
        validtill TIMESTAMP NOT NULL,
        FOREIGN KEY (userid) REFERENCES Users(userid)
            ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BannedUsers (
        emailid VARCHAR(64) PRIMARY KEY,
        reason TEXT
    
    );
    """)

    cursor.close()

def get_longlink(shortlink):
    cursor = connection.cursor()

    try:
        print(f"Looking for shortlink: '{shortlink}' of type {type(shortlink)}")

        query = "SELECT longlink FROM Links WHERE shortlink =%s"
        cursor.execute(query, (shortlink,))

        result = cursor.fetchone()
        print("Query result:", result)

        return result[0] if result else None

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None


def add_user(email, password, username):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT 1 FROM Users WHERE email = %s", (email,))
        if cursor.fetchone():
            return "user exists"

        userid = gen.generate_userid(cursor)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        cursor.execute("""
            INSERT INTO Users (userid, username, password, email)
            VALUES (%s, %s, %s, %s)
        """, (userid, username, hashed_password, email))
        return userid

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None


def db_verify_user(email, password):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT userid, password FROM Users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if not result:
            return "user does not exist"

        userid, hashed_password = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return userid
        else:
            return "incorrect password"

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None

def db_create_session(userid):
    cursor = connection.cursor()

    try:
        sessiontoken = gen.generate_sessiontoken(cursor)

        validtill = datetime.utcnow() + datetime.timedelta(days=30)

        cursor.execute("""
            INSERT INTO Sessions (sessiontoken, userid, validtill)
            VALUES (%s, %s, %s)
        """, (sessiontoken, userid, validtill))
        return sessiontoken

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None
    

def db_verify_session(sessiontoken):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT userid, validtill FROM Sessions WHERE sessiontoken = %s
        """, (sessiontoken,))
        result = cursor.fetchone()
        if not result:
            return "session does not exist"

        userid, validtill = result
        if validtill < datetime.utcnow():
            return "session does not exist"

        return userid

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None


def db_add_link(userid, shortlink, longlink):
    cursor = connection.cursor()

    try:
        if not shortlink:
            shortlink = gen.generate_shortlink(cursor)

        linkid = gen.generate_linkid(cursor)

        cursor.execute("""
            INSERT INTO Links (userid, linkid, shortlink, longlink, fingerprint)
            VALUES (%s, %s, %s, %s, %s)
        """, (userid, linkid, shortlink, longlink, False))
        return linkid

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None

def delete_link_by_id(linkid):
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Links WHERE id = %s", (linkid,))
        return cursor.rowcount > 0

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return False