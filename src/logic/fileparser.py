import csv

import pandas as pd
from docx import Document


def csv_to_list(path: str) -> list[str]:
    """
    Extracts the data from a csv file and returns it as a pandas dataframe
    """
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=";", quotechar="|")
        data = []
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].replace('"', "")
            data.append(row)
        ret = []
        for i in data:
            ret.append(i[0])
        return ret


def word_docx_to_csv(path) -> pd.DataFrame:
    doc = Document(path)
    tables = doc.tables

    m_data = []
    for table in tables:
        data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                text = cell.text
                text = text.replace("\n", "")
                row_data.append(text)
            data.append(row_data)
        df = pd.DataFrame(data)
        df.columns = df.iloc[0]
        df = df.iloc[1:]

        m_data.append(df)

    df = m_data[2]
    return df
