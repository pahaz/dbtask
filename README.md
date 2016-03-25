# gitdata module #
The module that able to import code from the github.

Example: `import gitdata.github.pahaz.users` где `import gitdata.<git-repo-doted-path>.<filename>`

Minimal example:

```
import gitdata.github.pahaz.dbtask as db
db.load(['users'])
assert db.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'
```

Full example:

```
import gitdata.github.pahaz.dbtask as db
db.load(['users'])
assert db.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'
db.users.append({"name": "NewUser"})
db.save(['users'])
```
