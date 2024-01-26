import datetime
import os
import re
import shutil
import sqlite3 as sql3
import tempfile
from typing import Any

from omegaconf import OmegaConf

from src.backend.db import main as template
# from src.data import pickles
import pickle
from src.logic.constants import SEMAP_MEDIA_ACCOUNTS
from src.logic.dataclass import ApparatData, BookData
from log import MyLogger
from icecream import ic
config = OmegaConf.load("config.yaml")

logger = MyLogger("Database")


class Database:
    logger.log_info("Database imported")

    def __init__(self) -> None:
        # TODO: change path later on to a variable based on the settings
        self.database_path = f"{config.database.path}{config.database.name}"
        ic(self.database_path)
        # self.database_path = "sap.db"
        logger.log_info("Connecting to database")
        self.database = sql3.connect(self.database_path)
        self.cur = self.database.cursor()

        pass
    def create_database(self):
        #create database from template
        template(self.database_path)
        subjects = config.subjects
        for subject in subjects:
            self.cur.execute(f"INSERT INTO subjects (name) VALUES ('{subject}')")
        self.database.commit()

    def create_blob(self, file):
        with open(file, "rb") as f:
            blob = f.read()
        return blob

    def recreate_file(self, filename, app_id: int):
        blob = self.get_blob(filename, app_id)
        # write the blob to the file and save it to a preset destination
        # with open(filename, "wb") as f:
        #     f.write(blob)
        #use tempfile to create a temporary file 
        if not os.path.exists(config.database.tempdir):
            os.mkdir(config.database.tempdir)
        tempfile.NamedTemporaryFile(filename=filename,delete=False,dir=config.database.tempdir,mode="wb").write(blob)
        
        # user = os.getlogin()
        # home = os.path.expanduser("~")

        # # check if the folder exists, if not, create it
        # if not os.path.exists(f"{home}/Desktop/SemApp/{user}"):
        #     os.mkdir(f"{home}/Desktop/SemApp/{user}")
        # shutil.move(filename, f"{home}/Desktop/SemApp/{user}")

    def get_blob(self, filename: str, app_id: int):
        query = f"SELECT fileblob FROM files WHERE filename='{filename}' AND app_id={app_id}"
        logger.log_info(f"Retrieving blob for {filename}, Appid {app_id} from database")
        result = self.cur.execute(query).fetchone()
        return result[0]

    def get_kto_no(self, app_id: int):
        query = f"SELECT konto FROM semesterapparat WHERE id={app_id}"
        result = self.cur.execute(query).fetchone()
        return result[0]

    def insert_file(self, file: list[dict], app_id: int, prof_id):
        for f in file:
            filename = f["name"]
            path = f["path"]
            filetyp = f["type"]
            print(f"filename: {filename}, path: {path}, filetyp: {filetyp}")
            if path == "Database":
                continue
            blob = self.create_blob(path)

            query = "INSERT OR IGNORE INTO files (filename, fileblob, app_id, filetyp,prof_id) VALUES (?, ?, ?, ?,?)"
            params = (filename, blob, app_id, filetyp, prof_id)
            self.cur.execute(query, params)
        logger.log_info(
            f"Inserted {len(file)} file(s) of Apparat {app_id} into database"
        )
        self.database.commit()

    def get_files(self, app_id: int, prof_id: int):
        query = f"SELECT filename, filetyp FROM files WHERE app_id={app_id} AND prof_id={prof_id}"
        result: list[tuple] = self.cur.execute(query).fetchall()
        return result

    def get_prof_name_by_id(self, id, add_title: bool = False):
        if add_title is True:
            query = f"SELECT titel, fname, lname FROM prof WHERE id={id}"
            result = self.cur.execute(query).fetchone()
            name = " ".join(result[0:3])
            return name
        else:
            query = f"SELECT fullname FROM prof WHERE id={id}"
            print(query)
            result = self.cur.execute(query).fetchone()
            name = result[0]
            return name

    def get_prof_id(self, profname: str):
        query = f"SELECT id FROM prof WHERE fullname='{profname.replace(',', '')}'"
        result = self.cur.execute(query).fetchone()
        if result is None:
            return None
        return self.cur.execute(query).fetchone()[0]

    def get_app_id(self, appname: str):
        query = f"SELECT id FROM semesterapparat WHERE name='{appname}'"
        result = self.cur.execute(query).fetchone()
        if result is None:
            return None
        return self.cur.execute(query).fetchone()[0]

    def get_profs(self):
        query = "select * from prof"
        return self.cur.execute(query).fetchall()

    def app_exists(self, appnr: str) -> bool:
        query = f"SELECT appnr FROM semesterapparat WHERE appnr='{appnr}'"
        result = self.cur.execute(query).fetchone()
        if result is None:
            return False
        return True

    def get_prof_data(self, profname: str = None, id: int = None) -> dict[str, str]:
        if profname is not None:
            profname = profname.replace(",", "")
            profname = re.sub(r"\s+", " ", profname).strip()
        if id:
            query = "Select prof_id FROM semesterapparat WHERE appnr=?"
            params = (id,)
            result = self.cur.execute(query, params).fetchone()
            id = result[0]
        query = (
            f"SELECT * FROM prof WHERE fullname='{profname}'"
            if id is None
            else f"SELECT * FROM prof WHERE id={id}"
        )
        result = self.cur.execute(query).fetchone()
        return_data = {
            "prof_title": result[1],
            "profname": f"{result[3], result[2]}",
            "prof_mail": result[5],
            "prof_tel": result[6],
            "id": result[0],
        }
        print(return_data)
        # select the entry that contains the first name
        return return_data

    def set_new_sem_date(self, appnr, new_sem_date, dauerapp=False):
        # Todo: use extend_semester in new release
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        query = f"UPDATE semesterapparat SET verlängert_am='{date}', verlängerung_bis='{new_sem_date}' WHERE appnr='{appnr}'"
        if dauerapp is not False:
            query = f"UPDATE semesterapparat SET verlängert_am='{date}', verlängerung_bis='{new_sem_date}', dauerapp='{dauerapp} WHERE appnr='{appnr}'"
        self.cur.execute(query)

        self.database.commit()

    def create_apparat(self, ApparatData: ApparatData):
        prof_id = self.get_prof_id(ApparatData.profname)
        app_id = self.get_app_id(ApparatData.appname)
        if app_id is None:
            if prof_id is None:
                self.create_prof(ApparatData.get_prof_details())
                prof_id = self.get_prof_id(ApparatData.profname)

            query = f"INSERT OR IGNORE INTO semesterapparat (appnr, name, erstellsemester, dauer, prof_id, fach,deletion_status,konto) VALUES ('{ApparatData.appnr}', '{ApparatData.appname}', '{ApparatData.semester}', '{ApparatData.dauerapp}', {prof_id}, '{ApparatData.app_fach}', '{ApparatData.deleted}', '{SEMAP_MEDIA_ACCOUNTS[ApparatData.appnr]}')"
            print(query)
            self.cur.execute(query)
            self.database.commit()
            logger.log_info(f"Created new apparat {ApparatData.appname}")
            app_id = self.get_app_id(ApparatData.appname)
            # if ApparatData.media_list is not None: #! Deprecated
            #     for media in ApparatData.media_list:
            #         self.insert_file(media, app_id)
            #     self.database.commit()
        return app_id

    def create_prof(self, prof_details: dict):
        prof_title = prof_details["prof_title"]
        prof_fname = prof_details["profname"].split(",")[1]
        prof_fname = prof_fname.strip()
        prof_lname = prof_details["profname"].split(",")[0]
        prof_lname = prof_lname.strip()
        prof_fullname = prof_details["profname"].replace(",", "")
        prof_mail = prof_details["prof_mail"]
        prof_tel = prof_details["prof_tel"]

        query = f'INSERT OR IGNORE INTO prof (titel, fname, lname, fullname, mail, telnr) VALUES ("{prof_title}", "{prof_fname}", "{prof_lname}", "{prof_fullname}", "{prof_mail}", "{prof_tel}")'
        self.cur.execute(query)
        self.database.commit()
        pass

    def get_apparat_nrs(self) -> list:
        try:
            self.cur.execute(
                "SELECT appnr FROM semesterapparat Where deletion_status=0"
            )
        except sql3.OperationalError:
            return []
        return [i[0] for i in self.cur.fetchall()]

    def get_all_apparts(self, deleted=0):

        self.cur.execute(
            f"SELECT * FROM semesterapparat WHERE deletion_status={deleted}"
        )
        return self.cur.fetchall()

    #
    def get_app_data(self, appnr, appname) -> ApparatData:
        result = self.cur.execute(
            f"SELECT * FROM semesterapparat WHERE appnr='{appnr}' AND name='{appname}'"
        ).fetchone()
        print(f"result: {result}")
        # app_id=result[0]
        data = ApparatData()
        data.appnr = appnr
        data.app_fach = result[3]
        data.appname = result[1]
        profname = self.get_prof_name_by_id(result[2])
        # set profname to lastname, firstname
        profname = f"{profname.split(' ')[0]}, {profname.split(' ')[1]}"
        data.profname = profname
        prof_data = self.get_prof_data(data.profname)
        data.prof_mail = prof_data["prof_mail"]
        data.prof_tel = prof_data["prof_tel"]
        data.prof_title = prof_data["prof_title"]
        data.erstellsemester = result[5]
        data.semester = result[8]
        data.deleted = result[9]
        data.apparat_adis_id = result[12]
        data.prof_adis_id = None

        print(data)
        # data.media_list=self.get_media(app_id)

        return data

    def add_medium(self, bookdata: BookData, app_id: str, prof_id: str, *args):
        # insert the bookdata into the media table
        # try to retrieve the bookdata from the media table, check if the to be inserted bookdata is already in the table for the corresponding apparat
        # if yes, do not insert the bookdata
        # if no, insert the bookdata
        t_query = (
            f"SELECT bookdata FROM media WHERE app_id={app_id} AND prof_id={prof_id}"
        )
        # print(t_query)
        result = self.cur.execute(t_query).fetchall()
        result = [pickle.loads(i[0]) for i in result]
        if bookdata in result:
            print("Bookdata already in database")
            # check if the book was deleted in the apparat
            query = (
                "SELECT deleted FROM media WHERE app_id=? AND prof_id=? AND bookdata=?"
            )
            params = (app_id, prof_id, pickle.dumps(bookdata))
            result = self.cur.execute(query, params).fetchone()
            if result[0] == 1:
                print("Book was deleted, updating bookdata")
                query = "UPDATE media SET deleted=0 WHERE app_id=? AND prof_id=? AND bookdata=?"
                params = (app_id, prof_id, pickle.dumps(bookdata))
                self.cur.execute(query, params)
                self.database.commit()
            return

        query = (
            "INSERT INTO media (bookdata, app_id, prof_id,deleted) VALUES (?, ?, ?,?)"
        )
        converted = pickle.dumps(bookdata)
        params = (converted, app_id, prof_id, 0)
        self.cur.execute(query, params)
        self.database.commit()

    def request_medium(self, app_id, prof_id, signature) -> int:
        query = "SELECT bookdata, id FROM media WHERE app_id=? AND prof_id=?"
        params = (app_id, prof_id)
        result = self.cur.execute(query, params).fetchall()
        books = [(i[1], pickle.loads(i[0])) for i in result]
        print(books)
        book = [i[0] for i in books if i[1].signature == signature]
        return book[0]

    def add_message(self, message: dict, user, appnr):
        def __get_user_id(user):
            query = "SELECT id FROM user WHERE username=?"
            params = (user,)
            result = self.cur.execute(query, params).fetchone()
            return result[0]

        user_id = __get_user_id(user)
        query = "INSERT INTO messages (message, user_id, remind_at) VALUES (?, ?, ?)"
        params = (message["message"], user_id, message["remind_at"])
        self.cur.execute(query, params)
        self.database.commit()

    def get_messages(self, date: str):
        def __get_user_name(id):
            query = "SELECT username FROM user WHERE id=?"
            params = (id,)
            result = self.cur.execute(query, params).fetchone()
            return result[0]

        query = f"SELECT * FROM messages WHERE remind_at='{date}'"
        result = self.cur.execute(query).fetchall()
        ret = [
            {
                "message": i[2],
                "user": __get_user_name(i[4]),
                "apparatnr": i[5],
                "id": i[0],
            }
            for i in result
        ]
        return ret

    def get_apparat_id(self, appname):
        query = f"SELECT appnr FROM semesterapparat WHERE name='{appname}'"
        result = self.cur.execute(query).fetchone()
        return result[0]
    
    
    def get_apparats_by_semester(self, semester: str):
        query = f"SELECT * FROM semesterapparat WHERE erstellsemester='{semester}'"
        result = self.cur.execute(query).fetchall()
        return result

    def get_semester(self) -> list[str]:
        query = "SELECT DISTINCT erstellsemester FROM semesterapparat"
        result = self.cur.execute(query).fetchall()
        return [i for i in result]

    def is_eternal(self, id):
        query = f"SELECT dauer FROM semesterapparat WHERE id={id}"
        result = self.cur.execute(query).fetchone()
        return result[0]

    def statistic_request(self, **kwargs: Any):
        def __query(query):
            result = self.cur.execute(query).fetchall()
            for result_a in result:
                orig_value = result_a
                prof_name = self.get_prof_name_by_id(result_a[2])
                # replace the prof_id with the prof_name
                result_a = list(result_a)
                result_a[2] = prof_name
                result_a = tuple(result_a)
                result[result.index(orig_value)] = result_a

            return result

        if "deletable" in kwargs.keys():
            query = f"SELECT * FROM semesterapparat WHERE deletion_status=0 AND dauer=0 AND (erstellsemester!='{kwargs['deletesemester']}' OR verlängerung_bis!='{kwargs['deletesemester']}')"
            return __query(query)

        if "dauer" in kwargs.keys():
            kwargs["dauer"] = kwargs["dauer"].replace("Ja", "1").replace("Nein", "0")
        query = "SELECT * FROM semesterapparat WHERE "
        for key, value in kwargs.items() if kwargs.items() is not None else {}:
            print(key, value)
            query += f"{key}='{value}' AND "
            print(query)
        # remove deletesemester part from normal query, as this will be added to the database upon deleting the apparat
        if "deletesemester" in kwargs.keys():
            query = query.replace(
                f"deletesemester='{kwargs['deletesemester']}' AND ", ""
            )
        if "endsemester" in kwargs.keys():
            if "erstellsemester" in kwargs.keys():
                query = query.replace(f"endsemester='{kwargs['endsemester']}' AND ", "")
                query = query.replace(
                    f"erstellsemester='{kwargs['erstellsemester']} AND ", "xyz"
                )
            else:
                query = query.replace(
                    f"endsemester='{kwargs['endsemester']}' AND ", "xyz"
                )
                print("replaced")
            query = query.replace(
                "xyz",
                f"(erstellsemester='{kwargs['endsemester']}' OR verlängerung_bis='{kwargs['endsemester']}') AND ",
            )
        #remove all x="" parts from the query where x is a key in kwargs
        
        query = query[:-5]
        print(query)
        return __query(query)

    def get_app_count_by_semester(self) -> tuple[list[str], list[int]]:
        """get the apparats created and deleted in the distinct semesters"""

        # get unique semesters
        query = "SELECT DISTINCT erstellsemester FROM semesterapparat"
        result = self.cur.execute(query).fetchall()
        semesters = [i[0] for i in result]
        created = []
        deleted = []
        for semester in semesters:
            query = f"SELECT COUNT(*) FROM semesterapparat WHERE erstellsemester='{semester}'"
            result = self.cur.execute(query).fetchone()
            created.append(result[0])
            query = f"SELECT COUNT(*) FROM semesterapparat WHERE deletion_status=1 AND deleted_date='{semester}'"
            result = self.cur.execute(query).fetchone()
            deleted.append(result[0])
        # store data in a tuple
        ret = []
        e_tuple = ()
        for sem in semesters:
            e_tuple = (
                sem,
                created[semesters.index(sem)],
                deleted[semesters.index(sem)],
            )
            ret.append(e_tuple)
        return ret
        # get the count of apparats created in the semesters

    def apparats_by_semester(self, semester: str):
        """Get a list of all created and deleted apparats in the given semester"""
        # get a list of apparats created and in the given semester
        query = f"SELECT name,prof_id FROM semesterapparat WHERE erstellsemester='{semester}'"
        result = self.cur.execute(query).fetchall()
        c_tmp = []
        for i in result:
            c_tmp.append((i[0], self.get_prof_name_by_id(i[1])))
        query = (
            f"SELECT name,prof_id FROM semesterapparat WHERE deleted_date='{semester}'"
        )
        result = self.cur.execute(query).fetchall()
        d_tmp = []
        for i in result:
            d_tmp.append((i[0], self.get_prof_name_by_id(i[1])))
        # group the apparats by prof
        c_ret = {}
        for i in c_tmp:
            if i[1] not in c_ret.keys():
                c_ret[i[1]] = [i[0]]
            else:
                c_ret[i[1]].append(i[0])
        d_ret = {}
        for i in d_tmp:
            if i[1] not in d_ret.keys():
                d_ret[i[1]] = [i[0]]
            else:
                d_ret[i[1]].append(i[0])
        return {"created": c_ret, "deleted": d_ret}

    def delete_message(self, message_id):
        query = "DELETE FROM messages WHERE id=?"
        params = (message_id,)
        self.cur.execute(query, params)
        self.database.commit()

    def delete_medium(self, title_id):
        # delete the bookdata from the media table
        query = "UPDATE media SET deleted=1 WHERE id=?"
        params = (title_id,)
        self.cur.execute(query, params)
        self.database.commit()
        pass

    def update_bookdata(self, bookdata: BookData, title_id):
        query = "UPDATE media SET bookdata=? WHERE id=?"
        converted = pickle.dumps(bookdata)
        params = (converted, title_id)
        self.cur.execute(query, params)
        self.database.commit()

    def get_specific_book(self, book_id):
        query = "SELECT bookdata FROM media WHERE id=?"
        params = (book_id,)
        result = self.cur.execute(query, params).fetchone()
        return pickle.loads(result[0])

    def get_media(self, app_id, prof_id, del_state=0) -> list[dict[int, BookData, int]]:
        """request media from database and return result as list.

        Args:
        ----
            - app_id (int): ID of the apparat
            - prof_id (int): ID of the prof
            - del_state (int, optional): If deleted books should be requested as well. 1 = yes 0 = no. Defaults to 0.

        Returns:
        -------
            - list[dict[int,BookData,int]]: Returns a list of dictionaries containing the bookdata, the id and the availability of the book in the following format:
        -------
        {"id": int,
        "bookdata": BookData,
        "available": int}
        """
        query = f"SELECT id,bookdata,available FROM media WHERE (app_id={app_id} AND prof_id={prof_id}) AND (deleted={del_state if del_state == 0 else '1 OR deleted=0'})"
        logger.log_info(f"Requesting media from database with query: {query}")
        result = self.cur.execute(query).fetchall()
        ret_result = []
        for result_a in result:
            ic(result_a)
            data = {"id": int, "bookdata": BookData, "available": int}
            data["id"] = result_a[0]
            data["bookdata"] = pickle.loads(result_a[1])
            data["available"] = result_a[2]
            ret_result.append(data)
        return ret_result

    def get_subjects_and_aliases(self):
        query = "SELECT subjects.name, aliases.name FROM subjects LEFT JOIN aliases ON subjects.id = aliases.subject_id"
        return self.cur.execute(query).fetchall()

    def get_subjects(self):
        query = "SELECT id,name FROM subjects"
        return self.cur.execute(query).fetchall()
    
    def get_aliases(self,subject_id):
        query = f"SELECT name FROM aliases WHERE subject_id={subject_id}"
        return self.cur.execute(query).fetchall()
    
    def add_subject(self,subject_name):
        query = f"INSERT INTO subjects (name) VALUES ('{subject_name}')"
        self.cur.execute(query)
        self.database.commit()
        
    def get_apparats_by_prof(self,prof_id):
        query = f"SELECT * FROM semesterapparat WHERE prof_id={prof_id}"
        return self.cur.execute(query).fetchall()
    def add_alias(self,alias_name,subject):
        query = f"SELECT id FROM subjects WHERE name='{subject}'"
        subject_id = self.cur.execute(query).fetchone()[0]
        query = f"INSERT INTO aliases (name,subject_id) VALUES ('{alias_name}',{subject_id})"
        self.cur.execute(query)
        self.database.commit()
    
    def update_apparat(self, apparat_data: ApparatData):
        data = apparat_data
        query = f"UPDATE semesterapparat SET name = ?, fach = ?, dauer = ?, prof_id = ? WHERE appnr = ?"
        params = (
            data.appname,
            data.app_fach,
            data.dauerapp,
            self.get_prof_id(data.profname),
            data.appnr,
        )
        print(query)
        self.cur.execute(query, params)
        self.database.commit()

    def delete_apparat(self, appnr: str, semester: str):
        # update the deletion status to 1 and the deleted_state to semester for the given apparat
        query = f"UPDATE semesterapparat SET deletion_status=1, deleted_date='{semester}' WHERE appnr='{appnr}'"
        self.cur.execute(query)
        self.database.commit()

    def get_book_id(self, bookdata: BookData, app_id: int, prof_id: int):
        query = "SELECT id FROM media WHERE bookdata=? AND app_id=? AND prof_id=?"
        params = (pickle.loads(bookdata), app_id, prof_id)
        result = self.cur.execute(query, params).fetchone()
        return result

    

    def set_availability(self, book_id, available):
        query = "UPDATE media SET available=? WHERE id=?"
        params = (available, book_id)
        self.cur.execute(query, params)
        self.database.commit()

    def get_latest_book_id(self):
        query = "SELECT id FROM media ORDER BY id DESC LIMIT 1"
        result = self.cur.execute(query).fetchone()
        return result[0]

    def close(self):
        self.database.close()

    def login(self, username, hashed_password) -> bool:
        # check if the user and password exist in the database
        # if yes, return True
        # if no, return False
        query = "SELECT salt FROM user WHERE username=?"
        params = (username,)
        result = self.cur.execute(query, params).fetchone()

        if result is None:
            return False
        salt = result[0]
        print(salt)
        query = "SELECT password FROM user WHERE username=?"
        params = (str(username),)
        result = self.cur.execute(query, params).fetchone()
        password = result[0]
        if password == f"{salt}{hashed_password}":
            return True
        else:
            return False

    # admin stuff below here
    def get_users(self):
        query = "SELECT * FROM user"
        return self.cur.execute(query).fetchall()

    def get_apparats(self) -> list[tuple]:
        query = "SELECT * FROM semesterapparat"
        return self.cur.execute(query).fetchall()

    def change_password(self, user, password):
        saltq = "SELECT salt FROM user WHERE username=?"
        params = (user,)
        salt = self.cur.execute(saltq, params).fetchone()[0]
        password = f"{salt}{password}"
        query = "UPDATE user SET password=? WHERE username=?"
        params = (password, user)
        self.cur.execute(query, params)
        self.database.commit()
        
    def get_role(self, username):
        query = "SELECT role FROM user WHERE username=?"
        params = (username,)
        result = self.cur.execute(query,params).fetchone()
        return result[0]
        
    def get_roles(self):
        query = "SELECT role FROM user"
        return self.cur.execute(query).fetchall()

    def create_user(self, username, password, role, salt):
        """Create a user based on passed data.

        Args:
        ----
            - username (str): Username to be used
            - password (str): the salted password
            - role (str): Role of the user
            - salt (str): a random salt for the user
        """
        query = "INSERT OR IGNORE INTO user (username, password, role, salt) VALUES (?, ?, ?, ?)"
        params = (username, password, role, salt)
        self.cur.execute(query, params)
        self.database.commit()

    def delete_user(self, user):
        query = "DELETE FROM user WHERE username=?"
        params = (user,)
        self.cur.execute(query, params)
        self.database.commit()
        
    def get_faculty_members(self,name:str=None):
        query = "SELECT titel, fname,lname,mail,telnr,fullname FROM prof"
        if name:
            query = query.replace(",fullname", "")
            query += f" WHERE fullname='{name}'"
        return self.cur.execute(query).fetchall()
    
    def update_faculty_member(self,data,oldlname,oldfname):
        placeholders = ', '.join(f"{k} = :{k}" for k in data.keys())
        sql = f"UPDATE prof SET {placeholders} WHERE lname = :oldlname AND fname = :oldfname"
        data["oldlname"] = oldlname
        data["oldfname"] = oldfname
        print(sql, data)
        self.cur.execute(sql, data)
        self.database.commit()
    
    def faculty_data(self,name):
        query = f"SELECT * FROM prof WHERE fullname='{name}'"
        result = self.cur.execute(query).fetchone()
        return result    
    
    def update_user(self,username, data:dict[str,str]):
        
        query = "UPDATE user SET "
        for key,value in data.items():
            if key == "username":
                continue
            query += f"{key}='{value}',"
        query = query[:-1]
        query += " WHERE username=?"
        params = (username,)
        
        self.cur.execute(query,params)
        self.database.commit()
        
    def check_username(self,username):
        query = "SELECT username FROM user WHERE username=?"
        params = (username,)
        result = self.cur.execute(query,params).fetchone()
        if result is None:
            return False
        return True
    def get_apparats_name(self, app_id,prof_id):
        query = f"SELECT name FROM semesterapparat WHERE appnr={app_id} AND prof_id={prof_id}"
        ic(query)
        result = self.cur.execute(query).fetchone()
        return result[0]
    
    def search_book(self, data:dict[str,str])->list[tuple[BookData,int]]:
        query = "SELECT * FROM media "
        result = self.database.execute(query).fetchall()
        ret = []
        #get length of data dict
        length = len(data)
        mode = 0
        if length == 1:
            if "signature" in data.keys():
                mode = 1
            elif "title" in data.keys():
                mode = 2
        elif length == 2:
            mode = 3
        else:
            return None
        print(len(result))
        for res in result:
            bookdata = pickle.loads(res[1])
            app_id = res[2]
            prof_id = res[3]
            #if signature and title present in dict:
            #if signature present in dict:
            if mode == 1:
                if data["signature"] in bookdata.signature:
                    ret.append((bookdata,app_id,prof_id))
            #if title present in dict:
            elif mode == 2:
                if data["title"] in bookdata.title:
                    ret.append((bookdata,app_id,prof_id))
            elif mode == 3:
                if data["signature"] in bookdata.signature and data["title"] in bookdata.title:
                    ret.append((bookdata,app_id,prof_id))
        return ret


if __name__ == "__main__":
    db = Database()
    print(db.login("kirchner", "loginpass"))
