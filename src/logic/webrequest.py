import requests
from bs4 import BeautifulSoup
from omegaconf import OmegaConf

from src.logic.dataclass import BookData
from src.logic.log import MyLogger
from src.transformers import ARRAYData, BibTeXData, COinSData, RDSData, RISData
#import sleep_and_retry decorator to retry requests
from ratelimit import limits, sleep_and_retry

logger = MyLogger(__name__)
config = OmegaConf.load("config.yaml")

API_URL = "https://rds.ibs-bw.de/phfreiburg/opac/RDSIndexrecord/{}/"
PPN_URL = 'https://rds.ibs-bw.de/phfreiburg/opac/RDSIndex/Search?lookfor="{}"+&type=AllFields&limit=10&sort=py+desc%2C+title'
TITLE = "RDS_TITLE"
SIGNATURE = "RDS_SIGNATURE"
EDITION = "RDS_EDITION"
ISBN = "RDS_ISBN"
AUTHOR = "RDS_PERSON"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}


class WebRequest:
    def __init__(self) -> None:
        """Request data from the web, and format it depending on the mode."""
        self.signature = None
        self.ppn = None
        self.data = None
        logger.log_info("Initialized WebRequest")

    def get_ppn(self, signature):
        self.signature = signature
        if "+" in signature:
            signature = signature.replace("+", "%2B")
        if "doi.org" in signature:
            signature = signature.split("/")[-1]
        url = PPN_URL.format(signature)
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")
        if soup.find("div", class_="media") is None:
            logger.log_error(f"No data found for {signature}")
            return self
        ppn = soup.find("div", class_="media").get("id")
        self.ppn = ppn
        return self

    def get_link_data(self):
        page = requests.get(PPN_URL.format(self.ppn))
        soup = BeautifulSoup(page.content, "html.parser")
        # find div that contains daia_ in the id
        # find the pre tag in that div
        # return the text
        # div = soup.find("div",id=lambda x: x and "daia_" in x)
        # pre = div.find("pre")
        return soup

    def get_data(self) -> list[str] | str:
        # url = API_URL.format(self.ppn)
        if self.ppn is None:
            logger.log_error("No PPN found")
            return "error"
        page = requests.get(API_URL.format(self.ppn))
        logger.log_info(f"Requesting data from {API_URL.format(self.ppn)}")
        logger.log_info(f"Status code: {page.status_code}")
        # print(page.content)
        soup = BeautifulSoup(page.content, "html.parser")
        pre_tag = soup.find_all("pre")
        # print(pre_tag)
        return_data = []

        if pre_tag:
            for tag in pre_tag:
                data = tag.text.strip()
                return_data.append(data)
            return return_data
        else:
            print("No <pre> tag found")
            logger.log_error("No <pre> tag found")
            return return_data


class BibTextTransformer:
    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.field = None
        # print(self.field)
        self.data = None
        # self.bookdata = BookData(**self.data)

    def get_data(self, data: list) -> str:
        RIS_IDENT = "TY  -"
        ARRAY_IDENT = "[kid]"
        COinS_IDENT = "ctx_ver"
        BIBTEX_IDENT = "@book"
        RDS_IDENT = "RDS ---------------------------------- "
        if self.mode == "RIS":
            for line in data:
                if RIS_IDENT in line:
                    self.data = line
        elif self.mode == "ARRAY":
            for line in data:
                if ARRAY_IDENT in line:
                    self.data = line
        elif self.mode == "COinS":
            for line in data:
                if COinS_IDENT in line:
                    self.data = line
        elif self.mode == "BibTeX":
            for line in data:
                if BIBTEX_IDENT in line:
                    self.data = line
        elif self.mode == "RDS":
            for line in data:
                if RDS_IDENT in line:
                    self.data = line
        return self

    def return_data(self, option=None) -> BookData:
        """Return Data to caller.

        Args:
            option (string, optional): Option for RDS as there are two filetypes. Use rds_availability or rds_data. Anything else gives a dict of both responses. Defaults to None.

        Returns:
            BookData: _description_
        """
        if self.mode == "ARRAY":
            return ARRAYData().transform(self.data)
        elif self.mode == "COinS":
            return COinSData().transform(self.data)
        elif self.mode == "BibTeX":
            return BibTeXData().transform(self.data)
        elif self.mode == "RIS":
            return RISData().transform(self.data)
        elif self.mode == "RDS":
            return RDSData().transform(self.data).return_data(option)


def cover(isbn):
    test_url = f"https://www.buchhandel.de/cover/{isbn}/{isbn}-cover-m.jpg"
    print(test_url)
    data = requests.get(test_url, stream=True)
    return data.content


def get_content(soup, css_class):
    return soup.find("div", class_=css_class).text.strip()


if __name__ == "__main__":
    print("main")
    link = "ZE 77000 W492"
    data = WebRequest().get_ppn(link).get_data()

    print(data)
    # # data.get_ppn("ME 3000 S186 (2)")
    # # print(data.ppn)
    # # desc=data.get_data()
    # # print(type(desc))
    # # print(desc)
    # txt = (
    #     BibTextTransformer("RIS")
    #     .get_data(WebRequest().get_ppn("ST 250 U42 (15)").get_data())
    #     .return_data()
    # )
    # print(txt)

    # print(data)
    # print(BibTextTransformer(data).bookdata)
