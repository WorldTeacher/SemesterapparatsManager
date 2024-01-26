# # # # tupl = (0, 0, 0, 0, 0, 0)


# # # # def change_value(index: int, state: int):
# # # #     global tupl
# # # #     tupl = list(tupl)
# # # #     print(len(tupl))
# # # #     tupl[index] = state
# # # #     tupl = tuple(tupl)


# # # # def check_validity() -> bool:
# # # #     global tupl
# # # #     if all(tupl):
# # # #         return True
# # # #     else:
# # # #         return False


# # # # print(tupl)
# # # # print(check_validity())
# # # # change_value(0, 1)
# # # # for i in range(1, 6):
# # # #     change_value(i, 1)
# # # # print(tupl)
# # # # print(check_validity())
# # # import sqlite3
# # # from codebase import Database
# # # # print(messages)

# # # def day_to_message(messages:list[dict[str]]):
# # #     print(messages)
# # #     ret = []
# # #     #extract the remind_at from each message and add them to ret. If the key already exists, append the message to the list
# # #     for message in messages:
# # #         print(message)
# # #         remind_at = message["remind_at"]
# # #         if remind_at in ret:
# # #             ret[remind_at].append(message)
# # #         else:
# # #             ret[remind_at] = [message]
# # #     print(ret)
# # # if __name__ =="__man__":
# # #     db = Database()

# # #     messages = db.get_messages()
# # #     print(messages)
# # #     print(day_to_message(messages))


# # from natsort import natsorted

# # unsorted = ["WiSe 23/24", "SoSe 23", "WiSe 21/22", "SoSe 21", "WiSe 22/23", "SoSe 22"]

# # def custom_sort(unsorted:list[str])->list[str]:
# #     """Sort a list of semesters in the format "SoSe n" and "WiSe n/n+1" in the correct order.
# #     Where n == year in 2 digit format

# #     Args:
# #         unsorted (list[str]): List of semesters in the format "SoSe n" and "WiSe n/n+1"

# #     Returns:
# #         ret (list[str]): Sorted list in correct order
# #     """
# #     #split the list into two lists, one with the summer semesters and one with the winter semesters
# #     summer = natsorted([ i for i in unsorted if "SoSe" in i])
# #     winter = natsorted([i for i in unsorted if "WiSe" in i])
# #     #merge the lists entries alternately
# #     ret = []
# #     for i in range(len(summer)):
# #         ret.append(summer[i])
# #         ret.append(winter[i])
# #     return ret
# from typing import Any
    
# def statistic_request(**kwargs:Any):
    
    
#     if "deletable" in kwargs.keys():
#         query = f"SELECT * FROM semesterapparat WHERE deletion_status=0 AND dauer=0 AND (erstellsemester!='{kwargs['deletesemester']}' OR verlängerung_bis!='{kwargs['deletesemester']}')"
#         return query
    
#     if "dauer" in kwargs.keys():
#         kwargs["dauer"] = kwargs["dauer"].replace("Ja", "1").replace("Nein", "0")
#     query = "SELECT * FROM semesterapparat WHERE "
#     for key, value in kwargs.items() if kwargs.items() is not None else {}:
#         print(key, value)
#         query += f"{key}='{value}' AND "
#         print(query)
#     #remove deletesemester part from normal query, as this will be added to the database upon deleting the apparat
#     if "deletesemester" in kwargs.keys(): 
#         query = query.replace(f"deletesemester='{kwargs['deletesemester']}' AND ", "")
#     if "endsemester" in kwargs.keys():
#         if "erstellsemester" in kwargs.keys():
#             query = query.replace(f"endsemester='{kwargs['endsemester']}' AND ", "")
#             query = query.replace(f"erstellsemester='{kwargs['erstellsemester']} AND ", "xyz")
#         else: 
#             query = query.replace(f"endsemester='{kwargs['endsemester']}' AND ", "xyz")
#             print("replaced")
#         query = query.replace("xyz", f"(erstellsemester='{kwargs['endsemester']}' OR verlängerung_bis='{kwargs['endsemester']}') AND ")
        
#     query = query[:-5].strip()
#     return query
# from threads import AutoAdder
# from PyQt6 import QtWidgets
# from ui import parsed_titles_ui
# import sys
# def main(data):
#     app = QtWidgets.QApplication(sys.argv)
#     dialog = QtWidgets.QDialog()
#     ui = parsed_titles_ui()
#     ui.setupUi(dialog)
#     ui.signatures = data
#     ui.app_id = 3
#     ui.prof_id = 1
#     ui.toolButton.click()
#     ui.populate_table()
#     ui.progressBar.setMaximum(len(data))
#     ui.progressBar.setValue(0)

#     dialog.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     data = ['YH 6876 S344', 'YM 3500 L925', 'CU 3200 W862', 'CW 6940 W842', 'CZ 1360 M379', 'CU 3800 V445', 'CU 3100 L948', 'CU 3200 H379 (3)', 'YC 7093 K95', 'CU 8590 E34 (2)', 'MS 6410 L744 (2)+1', 'CUS778', 'Psy K 120: 125 b', 'Psy L 170: 66', 'MR 2600 M474 (12)+16', 'Psy K 760: 19', 'Psy K 110: 92', 'Psy K 400: 45 a', 'CD 20/10,6']
#     main(data)

from src.backend.database import Database
import pickle
db = Database()

query="SELECT * from media where id=1"
_data = db.database.execute(query).fetchall()
var = _data[0][1]
print(pickle.loads(var))