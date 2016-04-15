#!/usr/bin/python3

# Computer #1
import gitdata.github.KVSrep.dbtask as db
db.load(['temp/users'])
assert db.temp.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'
db.temp.users.append({"name": "NewUser"})
db.save(['temp/users'])

# Computer #2
import gitdata.github.KVSrep.dbtask as dc
dc.load(['temp/users'])
assert db.temp.users == [{"name": "Pahaz"}, {"name": "Test"}, {"name": "NewUser"}], 'new users did not loaded'