#!/usr/bin/python3

import gitdata.github.KVSrep.dbtask as db
db.load(['users', 'temp/users'])
assert db.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'
db.temp.users.append({"name": "NewUser"})
print(db.temp.users)
print(db.users)
db.save(["temp/users"])