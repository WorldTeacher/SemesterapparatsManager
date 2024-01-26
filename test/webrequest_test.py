import pytest
from src.logic.webrequest import WebRequest
from src.logic.webrequest import BibTextTransformer
from src.logic.dataclass import BookData

def test_webdata_bibtexttransform(source_data:str="RIS"):
    request = WebRequest().get_ppn("ST 250 U42 (15) ").get_data()
    assert isinstance(request, list) is True
    assert len(request)>0
    model:BookData = BibTextTransformer(source_data).get_data(request).return_data()
    assert model is not None
    assert model.signature =="ST 250 U42 (15)"
    assert model.ppn == "1693321114"
    assert model.author == "Ullenboom, Christian"
    assert model.link == "https://rds.ibs-bw.de/phfreiburg/link?kid=1693321114"
    assert model.pages=="1246"
    assert model.publisher=="Rheinwerk Computing"
    
    

    
    
    