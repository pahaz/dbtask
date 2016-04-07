#!/usr/bin/python3

# Computer #1
import gitdata.github.pahaz.dbtask as db
db.load(['users'])
assert db.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'
db.users.append({"name": "NewUser"})
db.save(['users'])

# Computer #2
import gitdata.github.pahaz.dbtask as db
db.load(['users'])
assert db.users == [{"name": "Pahaz"}, {"name": "Test"}, {"name": "NewUser"}], 'new users did not loaded'