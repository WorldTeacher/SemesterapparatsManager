from src.backend.database_rewrite import Database


db = Database("semap.db")
print(db.query_db("SELECT * FROM subjects WHERE id=1"))