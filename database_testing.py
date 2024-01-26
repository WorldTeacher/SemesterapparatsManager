from src.backend.database import Database
from src.logic.dataclass import ApparatData

apparat = ApparatData()
apparat.appname = "testapparat123"
apparat.appnr = 155
apparat.dauerapp = True
apparat.profname = "Mustermanns, Max"
apparat.subject = "Physik"
apparat.semester = "SoSe 2021"


files = {"name": "test.png", "type": "png",
         "path": r"C:\Users\aky547\Desktop\test.png"}
db = Database()
# print(db.recreate_file("testfile.pdf",files,3))
# db.insert_file(files,3)
# recreate_file("test.pdf",files,1))#insert_file(files,1))
db.get_apparats_name(70)