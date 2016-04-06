#!/usr/bin/python3

import gitdata.github.KVSrep.dbtask as db
db.load(['users'])
assert db.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'
print(db.users)