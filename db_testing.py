from omegaconf import OmegaConf

from codebase import Database
from codebase.pickles import load_pickle, make_pickle
from webrequest import BibTextTransformer, WebRequest

config = OmegaConf.load("config.yaml")
db = Database()
# # # f = db.get_media(1, 1)
# # # dataclass_objects = []

# # # for dataclass_str in f:
# # #     print(f"dataclass {dataclass_str}")
# # #     # dataclass_obj = ast.literal_eval(dataclass_str[0])
# # #     dataclass_objects.append(dataclass_str)

# # # cla = BookData().from_string(dataclass_objects[0])
# # # print(type(cla))
# # book = (
# #     BibTextTransformer("ARRAY")
# #     .get_data(WebRequest().get_ppn("ST 250 U42 (15)").get_data())
# #     .return_data()
# # )
# # print(book)

# # bpickle = make_pickle(book)
# # print(bpickle)

# # print(load_pickle(bpickle))


# # # print(pickle.dumps(book), type(pickle.dumps(book)))

# # # db.add_medium(book, "2", "1")
# # # db.get_app_data("1", "Testapparat")

# # books = db.get_media(1, 1, 0)

# # print(len(books))
# book = db.get_specific_book(16)

# print(book)


if __name__ == "__main__":
    print(db.get_media(15, 2))
