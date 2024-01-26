import tabula


file="files/Semesterapparat - Anmeldung.pdf"

def extract_book_data(file):
    tables=tabula.read_pdf(file,pages="all",encoding="utf-8",multiple_tables=True)
    tabula.convert_into(file, file.replace(".pdf"), output_format="csv", pages="all")
    with open("files/Semesterapparat - Anmeldung.csv", "r") as f:
        content=f.read()
    
