import gitdata.github.larpy.dbtask as db

db.load(['users'])
print(db.users)
assert db.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'
db.users.append({"name": "NewUser"})
db.save(['users'])
print(db.users)
