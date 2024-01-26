import pandas as pd
from docx import Document


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
