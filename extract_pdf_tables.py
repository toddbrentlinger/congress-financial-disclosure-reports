import tabula

def extract_pdf_tables_tabula(filename):
    # Read pdf into list of DataFrame
    df = tabula.read_pdf(filename, pages='all', password='', format='JSON', stream=True)

    print(df)