from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text

data = {}

def decode_value(value):

    # decode PSLiteral, PSKeyword
    if isinstance(value, (PSLiteral, PSKeyword)):
        value = value.name

    # decode bytes
    if isinstance(value, bytes):
        value = decode_text(value)

    return value

def extract_acroform_from_pdf(filename):
    with open(filename, 'rb') as fp:
        parser = PDFParser(fp)

        doc = PDFDocument(parser)
        res = resolve1(doc.catalog)

        if 'AcroForm' not in res:
            raise ValueError("No AcroForm Found")

        fields = resolve1(doc.catalog['AcroForm'])['Fields']  # may need further resolving

        for f in fields:
            field = resolve1(f)
            name, values = field.get('T'), field.get('V')

            # decode name
            name = decode_text(name)

            # resolve indirect obj
            values = resolve1(values)

            # decode value(s)
            if isinstance(values, list):
                values = [decode_value(v) for v in values]
            else:
                values = decode_value(values)

            data.update({name: values})

            print(name, values)