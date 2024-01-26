CREATE_TABLE_APPARAT = """CREATE TABLE semesterapparat (
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
CREATE_TABLE_MEDIA = """CREATE TABLE media (
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
CREATE_TABLE_APPKONTOS = """CREATE TABLE app_kontos (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    app_id INTEGER,
    konto INTEGER,
    passwort TEXT,
    FOREIGN KEY (app_id) REFERENCES semesterapparat (id)
    )"""
CREATE_TABLE_FILES = """CREATE TABLE files (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    fileblob BLOB,
    app_id INTEGER,
    filetyp TEXT,
    prof_id INTEGER REFERENCES prof (id),
    FOREIGN KEY (app_id) REFERENCES semesterapparat (id)
    )"""
CREATE_TABLE_MESSAGES = """CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    created_at date NOT NULL DEFAULT CURRENT_TIMESTAMP,
    message TEXT NOT NULL,
    remind_at date NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    appnr INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
  )"""
CREATE_TABLE_PROF = """CREATE TABLE prof (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    titel TEXT,
    fname TEXT,
    lname TEXT,
    fullname TEXT NOT NULL UNIQUE,
    mail TEXT,
    telnr TEXT
  )"""
CREATE_TABLE_USER = """CREATE TABLE user (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT UNIQUE,
    name TEXT
  )"""
CREATE_TABLE_SUBJECTS = """CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE
)"""


