import sqlite3
from omegaconf import OmegaConf
config = OmegaConf.load("config.yaml")
subjects = config.subjects

# Connect to the database
def main(database):
    conn = sqlite3.connect(database)
    conn.execute(
      """CREATE TABLE app_kontos (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    app_id INTEGER,
    konto INTEGER,
    passwort TEXT,
    FOREIGN KEY (app_id) REFERENCES semesterapparat (id)
    )"""
    )

    conn.execute(
        """CREATE TABLE files (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    fileblob BLOB,
    app_id INTEGER,
    filetyp TEXT,
    prof_id INTEGER REFERENCES prof (id),
    FOREIGN KEY (app_id) REFERENCES semesterapparat (id)
    )"""
    )

    conn.execute(
        """CREATE TABLE media (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    bookdata BLOB,
    app_id INTEGER,
    prof_id INTEGER,
    deleted INTEGER DEFAULT (0),
    available BOOLEAN,
    reservation BOOLEAN,
    FOREIGN KEY (prof_id) REFERENCES prof (id),
    FOREIGN KEY (app_id) REFERENCES semesterapparat (id)
  )"""
    )

    conn.execute(
        """CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    created_at date NOT NULL DEFAULT CURRENT_TIMESTAMP,
    message TEXT NOT NULL,
    remind_at date NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    appnr INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
  )"""
    )

    conn.execute(
      """CREATE TABLE prof (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    titel TEXT,
    fname TEXT,
    lname TEXT,
    fullname TEXT NOT NULL UNIQUE,
    mail TEXT,
    telnr TEXT
  )"""
    )

    conn.execute(
        """CREATE TABLE semesterapparat (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT,
    prof_id INTEGER,
    fach TEXT,
    appnr INTEGER,
    erstellsemester TEXT,
    verlängert_am TEXT,
    dauer BOOLEAN,
    verlängerung_bis TEXT,
    deletion_status INTEGER,
    deleted_date TEXT,
    apparat_id_adis INTEGER,
    prof_id_adis INTEGER,
    konto INTEGER REFERENCES app_kontos (id),
    FOREIGN KEY (prof_id) REFERENCES prof (id)
  )"""
    )

    conn.execute(
        """CREATE TABLE user (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT UNIQUE,
    name TEXT
  )"""
    )
    conn.execute(
        """
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE
)
"""
    )

    conn.execute(
        """
                 CREATE TABLE aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    subject_id INTEGER,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
)
"""
    )

    # Commit the changes and close the connection
    conn.commit()
    #insert subjects
    
      
    conn.close()


if __name__ == "__main__":
    main()
