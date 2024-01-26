import datetime
import os
import re
import sqlite3 as sql
import tempfile
import pickle
from src.logic.log import MyLogger
from icecream import ic
from typing import List, Tuple, Dict, Any, Optional, Union
from omegaconf import OmegaConf
from src.backend.db import CREATE_TABLE_APPARAT, CREATE_TABLE_MESSAGES, CREATE_TABLE_MEDIA, CREATE_TABLE_APPKONTOS, CREATE_TABLE_FILES, CREATE_TABLE_MESSAGES, CREATE_TABLE_PROF, CREATE_TABLE_USER, CREATE_TABLE_SUBJECTS
from src.logic.constants import SEMAP_MEDIA_ACCOUNTS
from src.logic.dataclass import ApparatData, BookData

config = OmegaConf.load("config.yaml")
logger = MyLogger(__name__)

def load_pickle(data):
    return pickle.loads(data)
def dump_pickle(data):
    return pickle.dumps(data)
def create_blob(data):
    with open(data, "rb") as f:
        return f.read()
def create_file(filename:str, blob):
    with tempfile.TemporaryDirectory(delete=False) as tmpdir:
        filepath = os.path.join(tmpdir, filename)
        with open(filepath, "wb") as f:
            f.write(blob)
        return filepath

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = config.database.path
        else:
            self.db_path = db_path
        if self.get_db_contents() is None:
            self.create_tables()

    def get_db_contents(self):
        try:
            with sql.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
                return cursor.fetchall()
        except sql.OperationalError:
            return None
    
    def connect(self):
        return sql.connect(self.db_path)
    
    def close_connection(self, conn: sql.Connection):
        conn.close()
    
    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_APPARAT)
        cursor.execute(CREATE_TABLE_MESSAGES)
        cursor.execute(CREATE_TABLE_MEDIA)
        cursor.execute(CREATE_TABLE_APPKONTOS)
        cursor.execute(CREATE_TABLE_FILES)
        cursor.execute(CREATE_TABLE_PROF)
        cursor.execute(CREATE_TABLE_USER)
        cursor.execute(CREATE_TABLE_SUBJECTS)
        conn.commit()
        self.close_connection(conn)
        
    def query_db(self, query: str, args: Tuple = (), one: bool = False):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        rv = cursor.fetchall()
        conn.commit()
        self.close_connection(conn)
        return (rv[0] if rv else None) if one else rv
    
    
    

        
    
    
        
    
        