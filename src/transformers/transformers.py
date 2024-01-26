from __future__ import annotations

import json
import re
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from src.logic.dataclass import BookData
from log import MyLogger

logger = MyLogger("transformers.py")


###Pydatnic models
@dataclass
class Item:
    superlocation: str | None = dataclass_field(default_factory=str)
    status: str | None = dataclass_field(default_factory=str)
    availability: str | None = dataclass_field(default_factory=str)
    notes: str | None = dataclass_field(default_factory=str)
    limitation: str | None = dataclass_field(default_factory=str)
    duedate: str | None = dataclass_field(default_factory=str)
    id: str | None = dataclass_field(default_factory=str)
    item_id: str | None = dataclass_field(default_factory=str)
    ilslink: str | None = dataclass_field(default_factory=str)
    number: int | None = dataclass_field(default_factory=int)
    barcode: str | None = dataclass_field(default_factory=str)
    reserve: str | None = dataclass_field(default_factory=str)
    callnumber: str | None = dataclass_field(default_factory=str)
    department: str | None = dataclass_field(default_factory=str)
    locationhref: str | None = dataclass_field(default_factory=str)
    location: str | None = dataclass_field(default_factory=str)

    def from_dict(self, data: dict) -> self:
        """Import data from dict"""
        data = data["items"]
        for entry in data:
            for key, value in entry.items():
                setattr(self, key, value)
        return self


@dataclass
class RDS_AVAIL_DATA:
    """Class to store RDS availability data"""

    library_sigil: str = dataclass_field(default_factory=str)
    items: List[Item] = dataclass_field(default_factory=list)

    def import_from_dict(self, data: str) -> self:
        """Import data from dict"""
        edata = json.loads(data)
        # library sigil is first key

        self.library_sigil = str(list(edata.keys())[0])
        # get data from first key
        edata = edata[self.library_sigil]
        for location in edata:
            item = Item(superlocation=location).from_dict(edata[location])

            self.items.append(item)
        return self


@dataclass
class RDS_DATA:
    """Class to store RDS data"""

    RDS_SIGNATURE: str = dataclass_field(default_factory=str)
    RDS_STATUS: str = dataclass_field(default_factory=str)
    RDS_LOCATION: str = dataclass_field(default_factory=str)
    RDS_URL: Any = dataclass_field(default_factory=str)
    RDS_HINT: Any = dataclass_field(default_factory=str)
    RDS_COMMENT: Any = dataclass_field(default_factory=str)
    RDS_HOLDING: Any = dataclass_field(default_factory=str)
    RDS_HOLDING_LEAK: Any = dataclass_field(default_factory=str)
    RDS_INTERN: Any = dataclass_field(default_factory=str)
    RDS_PROVENIENCE: Any = dataclass_field(default_factory=str)
    RDS_LOCAL_NOTATION: str = dataclass_field(default_factory=str)
    RDS_LEA: Any = dataclass_field(default_factory=str)

    def import_from_dict(self, data: dict) -> RDS_DATA:
        """Import data from dict"""
        for key, value in data.items():
            setattr(self, key, value)
        return self


@dataclass
class RDS_GENERIC_DATA:
    LibrarySigil: str = dataclass_field(default_factory=str)
    RDS_DATA: List[RDS_DATA] = dataclass_field(default_factory=list)

    def import_from_dict(self, data: str) -> RDS_GENERIC_DATA:
        """Import data from dict"""
        edata = json.loads(data)
        # library sigil is first key
        self.LibrarySigil = str(list(edata.keys())[0])
        # get data from first key
        edata = edata[self.LibrarySigil]
        for entry in edata:
            rds_data = RDS_DATA()  # Create a new RDS_DATA instance
            # Populate the RDS_DATA instance from the entry
            # This assumes that the entry is a dictionary that matches the structure of the RDS_DATA class
            rds_data.import_from_dict(entry)
            self.RDS_DATA.append(rds_data)  # Add the RDS_DATA instance to the list
        return self


class BaseStruct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ARRAYData:
    def __init__(self):
        pass

    def transform(self, data: str) -> BookData:
        def _get_line(source: str, search: str) -> str:
            try:
                return (
                    source.split(search)[1]
                    .split("\n")[0]
                    .strip()
                    .replace("=>", "")
                    .strip()
                )

            except Exception as e:
                logger.log_exception("ARRAYData.transform failed")
                return ""

        def _get_list_entry(source: str, search: str, entry: str) -> str:
            try:
                source = source.replace("\t", "").replace("\r", "")
                source = source.split(search)[1].split(")")[0]
                return _get_line(source, entry).replace("=>", "").strip()
            except:
                return ""

        def _get_isbn(source: str) -> list:
            try:
                isbn = source.split("[isbn]")[1].split(")")[0].strip()
                isbn = isbn.split("(")[1]
                isbns = isbn.split("=>")
                ret = []
                for _ in isbns:
                    # remove _ from list
                    isb = _.split("\n")[0].strip()
                    if isb == "":
                        continue
                    ret.append(isb) if isb not in ret else None
                return ret
            except:
                isbn = []
                return isbn

        return BookData(
            ppn=_get_line(data, "[kid]"),
            title=_get_line(data, "[ti_long]").split("/")[0].strip(),
            author=_get_list_entry(data, "[au]", "[0]"),
            edition=_get_list_entry(data, "[ausgabe]", "[0]").replace(",", ""),
            link=f"https://rds.ibs-bw.de/phfreiburg/link?kid={_get_line(data,'[kid]')}",
            isbn=_get_isbn(data),
            # [self._get_list_entry(data,"[isbn]","[0]"),self._get_list_entry(data,"[is]","[1]")],
            language=_get_list_entry(data, "[la_facet]", "[0]"),
            publisher=_get_list_entry(data, "[hg]", "[0]"),
            year=_get_line(data, "[py]"),
            pages=_get_list_entry(data, "[umfang]", "[0]").split(":")[0].strip(),
        )


class COinSData:
    def __init__(self) -> None:
        pass

    def transform(self, data: str) -> BookData:
        def _get_line(source: str, search: str) -> str:
            try:
                data = source.split(f"{search}=")[1]  # .split("")[0].strip()
                return data.split("rft")[0].strip() if "rft" in data else data
            except:
                return ""

        return BookData(
            ppn=_get_line(data, "rft_id").split("=")[1],
            title=_get_line(data, "rft.btitle"),
            author=f"{_get_line(data,'rft.aulast')}, {_get_line(data,'rft.aufirst')}",
            edition=_get_line(data, "rft.edition"),
            link=_get_line(data, "rft_id"),
            isbn=_get_line(data, "rft.isbn"),
            publisher=_get_line(data, "rft.pub"),
            year=_get_line(data, "rft.date"),
            pages=_get_line(data, "rft.tpages").split(":")[0].strip(),
        )


class RISData:
    def __init__(self) -> None:
        pass

    def transform(self, data: str) -> BookData:
        def _get_line(source: str, search: str) -> str:
            try:
                data = source.split(f"{search}  - ")[1]  # .split("")[0].strip()
                return data.split("\n")[0].strip() if "\n" in data else data
            except:
                return ""

        return BookData(
            ppn=_get_line(data, "DP").split("=")[1],
            title=_get_line(data, "TI"),
            signature=_get_line(data, "CN"),
            edition=_get_line(data, "ET").replace(",", ""),
            link=_get_line(data, "DP"),
            isbn=_get_line(data, "SN").split(","),
            author=_get_line(data, "AU").split("[")[0].strip(),
            language=_get_line(data, "LA"),
            publisher=_get_line(data, "PB"),
            year=_get_line(data, "PY"),
            pages=_get_line(data, "SP"),
        )


class BibTeXData:
    def __init__(self):
        pass

    def transform(self, data: str) -> BookData:
        def _get_line(source: str, search: str) -> str:
            try:
                return (
                    data.split(search)[1]
                    .split("\n")[0]
                    .strip()
                    .split("=")[1]
                    .strip()
                    .replace("{", "")
                    .replace("}", "")
                    .replace(",", "")
                    .replace("[", "")
                    .replace("];", "")
                )
            except:
                return ""

        return BookData(
            ppn=None,
            title=_get_line(data, "title"),
            signature=_get_line(data, "bestand"),
            edition=_get_line(data, "edition"),
            isbn=_get_line(data, "isbn"),
            author=";".join(_get_line(data, "author").split(" and ")),
            language=_get_line(data, "language"),
            publisher=_get_line(data, "publisher"),
            year=_get_line(data, "year"),
            pages=_get_line(data, "pages"),
        )


class RDSData:
    retlist = []

    def transform(self, data: str):
        # rds_availability = RDS_AVAIL_DATA()
        # rds_data = RDS_GENERIC_DATA()
        def __get_raw_data(data: str) -> list:
            # create base data to be turned into pydantic classes
            data = data.split("RDS ----------------------------------")[1]
            edata = data.strip()
            edata = edata.split("\n", 9)[9]
            edata = edata.split("\n")[1:]
            entry_1 = edata[0]
            edata = edata[1:]
            entry_2 = "".join(edata)
            edata = []
            edata.append(entry_1)
            edata.append(entry_2)
            return edata

        ret_data = __get_raw_data(data)
        # assign data[1] to RDS_AVAIL_DATA
        # assign data[0] to RDS_DATA
        self.rds_data = RDS_GENERIC_DATA().import_from_dict(ret_data[1])
        self.rds_availability = RDS_AVAIL_DATA().import_from_dict(ret_data[0])
        self.retlist.append(self.rds_availability)
        self.retlist.append(self.rds_data)
        return self

    def return_data(self, option=None):
        if option == "rds_availability":
            return self.retlist[0]
        elif option == "rds_data":
            return self.retlist[1]
        else:
            return {"rds_availability": self.retlist[0], "rds_data": self.retlist[1]}


if __name__ == "__main__":
    with open("daiadata", "r") as f:
        data = f.read()

    ret = RDSData().transform(data)
    data = ret.return_data("rds_availability")
    print(data)
