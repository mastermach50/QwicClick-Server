# Data Structure
## Tables
### Users
```
userid string 64
username string 64
password string 128
email string 64
```
### Links
```
userid string 64
linkid string 64
shortlink string 64
longlink string 64
fingerprint bool  // should the server fingerprint the client or just serve the redirection
```
### Sessions
```
userid string 64
sessiontoken string 64
validtill timestamp
```

# Functions to be implemented
```
db_add_user(email, password)
    // error if email already exists - return "user exists"
    // hash password using bcrypt
    // auto generate a 64 character userid that does not exist in the db
    // two random words and a number as username eg: bleached-sunshine-53 
    return userid

db_add_link(userid, shortlink, longlink)
    // if shortlink empty then autogenerate an 8 character shortlink
    // auto generate a 64 character linkid that does not exist in the db
    // set fingerprint to false by default
    return linkid

db_expand_link(shortlink)
    // error if link does not exist in db - return "link does not exist"
    // return longlink

db_delete_link(linkid)
    // delete the link entry from the links table

db_verify_user(email, password)
    // error if user does not exist - return "user does not exist"
    // verify the password against the stored hash in the db
    // return userid

db_create_session(userid)
    // generate 64 character random string as session token
    // set the valid till to one month later
    // save to sessions table
    return sessiontoken

db_verify_session(sessiontoken)
    // error if session does not exist - return "session does not exist"
    return userid
```