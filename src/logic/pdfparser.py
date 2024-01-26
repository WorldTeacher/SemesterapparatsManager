# add depend path to system path
import os
import sys

import pandas as pd
from pdfquery import PDFQuery


def pdf_to_csv(path: str) -> pd.DataFrame:
    """
    Extracts the data from a pdf file and returns it as a pandas dataframe
    """
    file = PDFQuery(path)
    file.load()
    #get the text from the pdf file
    text_elems = file.extract([
        ('with_formatter', 'text'),
        ('all_text', '*')
    ])
    extracted_text = text_elems['all_text']
    
    return extracted_text
    
    
if __name__ == "__main__":
    text = pdf_to_csv("54_pdf.pdf")
    #remove linebreaks
    text = text.replace("\n", "")
    print(text)
    
