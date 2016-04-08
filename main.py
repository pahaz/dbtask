import gitimport
gitimport.git_import()
import gitdata.github.lemarck.dbtask as db


def main():
    db.load(['users'])
    print(db.users)
    assert db.users == [{"name": "Pahaz"}, {"name": "Test"}], 'users did not loaded'


if __name__ == "__main__":
    main()