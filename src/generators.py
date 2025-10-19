import random
from uuid import uuid4

catsanddogs = [
    "beagle","borzoi","boxer","collie","corgie","dachshund","dingo","feist","harrier","hound","husky","maltese","pinscher","poodle","pug","retriever","rottweiler","schnauzer","setter","shepherd","spaniel","spitz","terrier","westie","whippet",
    "angora","balinese","bengal","birman","bobtail","bombay","burmese","calico","ginger","himalayan","javanese","korat","longhair","marmalade","oriental","persian","siamese","siberian","tabby","tom"
]

size = [
    "average","big","broad","flat","giant","huge","humongous","immense","large","little","long","massive","medium","miniature","short","small","tall","tiny","wide"
]

emotion = [
    "afraid","angry","calm","cheerful","cold","crabby","crazy","cross","excited","frigid","furious","glad","glum","happy","icy","jolly","jovial","kind","lively","livid","mad","ornery","rosy","sad","scared","seething","shy","sunny","tense","tranquil","upbeat","wary","weary","worried",
]

def random_string():
    return random.choice(size) + "-" + random.choice(emotion) + "-" + random.choice(catsanddogs)

def uuid():
    return str(uuid4())

def generate_userid(cursor):
    while True:
        userid = uuid()
        cursor.execute("SELECT 1 FROM Users WHERE userid = %s", (userid,))
        if not cursor.fetchone():
            return userid

def generate_linkid(cursor):
    while True:
        linkid = uuid()
        cursor.execute("SELECT 1 FROM Links WHERE linkid = %s", (linkid,))
        if not cursor.fetchone():
            return linkid

def generate_shortlink(cursor):
    while True:
        shortlink = random_string()
        cursor.execute("SELECT 1 FROM Links WHERE shortlink = %s", (shortlink,))
        if not cursor.fetchone():
            return shortlink

def generate_sessiontoken(cursor):
    while True:
        sessiontoken = uuid()
        cursor.execute("SELECT 1 FROM Sessions WHERE sessiontoken = %s", (sessiontoken,))
        if not cursor.fetchone():
            return sessiontoken


if __name__ == "__main__":
    print(random_string())
    print(uuid())