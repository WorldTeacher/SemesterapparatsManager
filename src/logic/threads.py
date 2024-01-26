import threading
import time

from PyQt6.QtCore import QThread, pyqtSignal

from src.backend.database import Database
from src.logic.log import MyLogger
from src.transformers import RDS_AVAIL_DATA
from src.logic.webrequest import BibTextTransformer, WebRequest
import sqlite3

class BookGrabber(QThread):
    updateSignal = pyqtSignal(int, int)

    def __init__(
        self,
        mode: str = None,
        data: list = None,
        app_id: int = None,
        prof_id: int = None,
        parent=None,
    ):
        super().__init__(parent)
        self.logger = MyLogger("Worker")
        self.logger.log_info("Starting worker thread")
        self.logger.log_info("Worker thread started")
        self.app_id = app_id
        self.prof_id = prof_id
        self.mode = mode
        self.data = data
        self.book_id = None
        self.db_lock = threading.Lock()

    def run(self):
        self.db = Database()
        item = 0
        for entry in self.data:
            signature = str(entry)
            self.logger.log_info("Processing entry: " + signature)

            webdata = WebRequest().get_ppn(entry).get_data()
            if webdata == "error":
                continue
            bd = BibTextTransformer(self.mode).get_data(webdata).return_data()
            transformer = BibTextTransformer("RDS")
            rds = transformer.get_data(webdata).return_data("rds_availability")
            bd.signature = entry
            with self.db_lock:
                #confirm lock is acquired 
                print("lock acquired, adding book to database")
                self.db.add_medium(bd, self.app_id, self.prof_id)
                # get latest book id
                self.book_id = self.db.get_latest_book_id()
            self.logger.log_info("Added book to database")
            state = 0
            for rds_item in rds.items:
                sign = rds_item.superlocation
                loc = rds_item.location
                # print(item.location)
                if self.app_id in sign or self.app_id in loc:
                    state = 1
                book_id = None
                # for book in self.books:
                #     if book["bookdata"].signature == entry:
                #         book_id = book["id"]
                #         break
                self.logger.log_info(f"State of {signature}: {state}")
                with self.db_lock:
                    print(
                        "lock acquired, updating availability of "
                        + str(book_id)
                        + " to "
                        + str(state)
                    )
                    try:
                        self.db.set_availability(self.book_id, state)
                    except sqlite3.OperationalError as e:
                        self.logger.log_error(f"Failed to update availability: {e}")
                    break

            # time.sleep(5)
            item += 1
            self.updateSignal.emit(item, len(self.data))
        self.logger.log_info("Worker thread finished")
        # teminate thread

        self.quit()


class AvailChecker(QThread):
    updateSignal = pyqtSignal(str, int)

    def __init__(
        self, links: list = [], appnumber: int = None, parent=None, books=list[dict]
    ):
        if links is None:
            links = []
        super().__init__(parent)
        self.logger = MyLogger("AvailChecker")
        self.logger.log_info("Starting worker thread")
        self.logger.log_info(
            "Checking availability for "
            + str(links)
            + " with appnumber "
            + str(appnumber)
            + "..."
        )
        self.links = links
        self.appnumber = appnumber
        self.books = books
        self.db_lock = threading.Lock()

    def run(self):
        self.db = Database()
        state = 0

        for link in self.links:
            self.logger.log_info("Processing entry: " + str(link))
            data = WebRequest().get_ppn(link).get_data()
            transformer = BibTextTransformer("RDS")
            rds = transformer.get_data(data).return_data("rds_availability")
            print(rds)
            for item in rds.items:
                sign = item.superlocation
                loc = item.location
                # print(item.location)
                if self.appnumber in sign or self.appnumber in loc:
                    state = 1
                book_id = None
                for book in self.books:
                    if book["bookdata"].signature == link:
                        book_id = book["id"]
                        break
                self.logger.log_info(f"State of {link}: " + str(state))
                with self.db_lock:
                    print(
                        "lock acquired, updating availability of "
                        + str(book_id)
                        + " to "
                        + str(state)
                    )
                    self.db.set_availability(book_id, state)
                    break
                self.updateSignal.emit(item.callnumber, state)

        self.logger.log_info("Worker thread finished")
        # teminate thread

        self.quit()


class AutoAdder(QThread):
    updateSignal = pyqtSignal(int)

    setTextSignal = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self, data=None, app_id=None, prof_id=None, parent=None):
        super().__init__(parent)
        self.logger = MyLogger("AutoAdder")
        self.data = data
        self.app_id = app_id
        self.prof_id = prof_id

        print("Launched AutoAdder")
        print(self.data, self.app_id, self.prof_id)

    def run(self):
        self.db = Database()
        # show the dialog, start the thread to gather data and dynamically update progressbar and listwidget
        self.logger.log_info("Starting worker thread")
        item = 0
        for entry in self.data:
            try:
                # webdata = WebRequest().get_ppn(entry).get_data()
                # bd = BibTextTransformer("ARRAY").get_data(webdata).return_data()
                # bd.signature = entry
                self.updateSignal.emit(item)
                self.setTextSignal.emit(entry)
                # qsleep
                item += 1
                self.progress.emit(item)
                print(item, len(self.data))
                time.sleep(1)

            except Exception as e:
                print(e)
                self.logger.log_exception(
                    f"The query failed with message {e} for signature {entry}"
                )
                continue
        if item == len(self.data):
            self.logger.log_info("Worker thread finished")
            # teminate thread
            self.finished.emit()
