from datetime import datetime, timedelta
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
        autocommit=True,
        database='qwicclick'
    )

def disconnect():
    global connection
    connection.close()

def initialize():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1204', 
        autocommit=True,
    )
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
        count INTEGER DEFAULT 0,
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
    connection.close()

def get_longlink(shortlink):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT linkid, longlink FROM Links WHERE shortlink =%s", (shortlink,))

        result = cursor.fetchone()
        (linkid, longlink) = result
        print(f"{shortlink} query result: {linkid} {longlink}")

        cursor.close()
        if not result:
            return "link does not exist"

        return result

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None

def increment_count(linkid):
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE Links SET count = count + 1 WHERE linkid = %s", (linkid,))

        cursor.close()
        return cursor.rowcount > 0
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

        cursor.close()
        return userid

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None


def verify_user(email, password):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT userid, password FROM Users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()

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

def create_session(userid):
    cursor = connection.cursor()

    try:
        sessiontoken = gen.generate_sessiontoken(cursor)

        validtill = datetime.utcnow() + timedelta(days=30)

        cursor.execute("""
            INSERT INTO Sessions (sessiontoken, userid, validtill)
            VALUES (%s, %s, %s)
        """, (sessiontoken, userid, validtill))

        cursor.close()
        return sessiontoken

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None


def verify_session(sessiontoken):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT userid, validtill FROM Sessions WHERE sessiontoken = %s", (sessiontoken,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return "session does not exist"

        userid, validtill = result
        if validtill < datetime.utcnow():
            return "session does not exist"

        return userid

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None


def add_link(userid, shortlink, longlink):
    cursor = connection.cursor()

    try:
        if not shortlink:
            shortlink = gen.generate_shortlink(cursor)

        cursor.execute("SELECT 1 FROM Links WHERE shortlink = %s", (shortlink,))
        if cursor.fetchone():
            return "shortlink already exists"

        linkid = gen.generate_linkid(cursor)

        cursor.execute("""
            INSERT INTO Links (userid, linkid, shortlink, longlink, fingerprint)
            VALUES (%s, %s, %s, %s, %s)
        """, (userid, linkid, shortlink, longlink, False))

        cursor.close()
        return (linkid, shortlink, longlink)

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None

def update_link(linkid, new_shortlink, new_longlink):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Links
            SET shortlink = %s, longlink = %s
            WHERE linkid = %s;
        """, (new_shortlink, new_longlink, linkid,))

        cursor.close()
        return cursor.rowcount > 0

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return False

def delete_link(linkid):
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Links WHERE linkid = %s", (linkid,))

        cursor.close()
        return cursor.rowcount > 0

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return False

# def get_link_info(linkid):
#     cursor = connection.cursor()

#     try:
#         cursor.execute("SELECT linkid, shortlink, longlink FROM Links WHERE linkid = %s", (linkid,))
#         result = cursor.fetchone()

#         if not result:
#             return "link does not exist"

#         linkid, shortlink, longlink = result

#         cursor.close()
#         return (linkid, shortlink, longlink)

#     except pymysql.MySQLError as err:
#         print(f"MySQL Error: {err}")
#         return None


def get_all_links(userid):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT linkid, shortlink, longlink FROM Links WHERE userid = %s", (userid,))
        result = cursor.fetchall()

        if not result:
            return []

        links = []
        for row in result:
            linkid, shortlink, longlink = row
            links.append({"linkid": linkid, "shortlink": shortlink, "longlink": longlink})

        cursor.close()
        return links

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None

def get_link_stats(linkid):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT count FROM Links WHERE linkid = %s", (linkid,))
        result = cursor.fetchone()

        if not result:
            return "link does not exist"

        cursor.close()
        return int(result[0])
    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None


def get_user_info(userid):
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT username, email FROM Users WHERE userid = %s", (userid,))
        result = cursor.fetchone()

        if not result:
            return "user does not exist"

        username, email = result

        cursor.close()
        return (username, email)

    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
        return None