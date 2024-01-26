import re
from dataclasses import dataclass, field


@dataclass
class ApparatData:
    prof_title: str | None = None
    profname: str | None = None
    dauerapp: bool = False
    appnr: int | None = None
    appname: str | None = None
    app_fach: str | None = None
    semester: str | None = None
    erstellsemester: str | None = None
    prof_mail: str | None = None
    prof_tel: int | None = None
    deleted: int = 0
    prof_adis_id: int | None = None
    apparat_adis_id: int | None = None

    def get_prof_details(self) -> dict:
        return {
            "prof_title": self.prof_title,
            "profname": self.profname,
            "prof_mail": self.prof_mail,
            "prof_tel": self.prof_tel,
            "fullname": self.profname,
        }


@dataclass
class BookData:
    ppn: str | None = None
    title: str | None = None
    signature: str | None = None
    edition: str | None = None
    link: str | None = None
    isbn: str | list | None = field(default_factory=list)
    author: str | None = None
    language: str | list | None = field(default_factory=list)
    publisher: str | None = None
    year: str | None = None
    pages: str | None = None
    # avaliability: dict | None = field(default_factory=dict)
    # def assign(self, field,value):
    #     self.__setattr__(field,value)

    def from_dict(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self):
        return self.__dict__

    def from_dataclass(self, dataclass):
        for key, value in dataclass.__dict__.items():
            setattr(self, key, value)

    def from_string(self, data: str):
        if not data.startswith("BookData"):
            raise ValueError("No valid BookData string")
        else:
            pattern = r"(\w+)='([^']*)'"
            data_dict = dict(re.findall(pattern, data))
            print(data_dict)
        for key, value in data_dict.items():
            setattr(self, key, value)
        return self


@dataclass
class MailData:
    subject: str | None = None
    body: str | None = None
    mailto: str | None = None
    prof: str | None = None
