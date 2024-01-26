from src.backend.database import Database
import pickle
def test_connection():
    db=Database()
    assert db.database is not None
    
def test_insert():
    db=Database()
    assert db.database is not None
    db.create_user("test_account", "test", "test", "test")
    curr_users = db.get_users()
    curr_users = [x[2] for x in curr_users]
    assert "test_account" in curr_users
    db.delete_user("test_account")
    curr_users = db.get_users()
    curr_users = [x[2] for x in curr_users]
    assert "test_account" not in curr_users
    
def test_pickle_bookdata():
    db=Database()
    assert db.database is not None
    