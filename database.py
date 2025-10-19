import pymysql

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