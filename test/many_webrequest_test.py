from test.webrequest_test import test_webdata_bibtexttransform


def many_test_webdata():
    test_webdata_bibtexttransform("RIS")
    test_webdata_bibtexttransform("BibTeX")
    test_webdata_bibtexttransform("COinS")
    test_webdata_bibtexttransform("ARRAY")
    test_webdata_bibtexttransform("RDS")
    assert True is True