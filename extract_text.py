import io
import sys
from pdfminer import pdfparser
if sys.version_info > (3,0):
    from io import StringIO
else:
    from io import BytestIO as StringIO

import requests
import PyPDF2

# pdfminer
from pdfminer import high_level
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from extract_pdf_tables import extract_pdf_tables_tabula

def extractTextFromPDFUsingPDFMiner(filename):
    output_string = StringIO()
    with open(filename, 'rb') as fin:
        parser = PDFParser(fin)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    print(output_string.getvalue())
    return output_string.getvalue()

def extractTextFromPDF(filename):
    if filename.startswith('http'):
        req = requests.get(filename)
        extractedText = high_level.extract_text(io.BytesIO(req.content), "")
    else:
        extractedText = high_level.extract_text(filename, "")
    
    print(extractedText)
    return extractedText

def extractTextFromPDFURL(url):
    pass

def extractTextFromPDFOld(filename):
    # create pdf file object
    pdfFileObj = open(filename, 'rb')

    # create a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Decrypt if needed
    if pdfReader.isEncrypted:
        pdfReader.decrypt('')

    # create a page object
    pageObj = pdfReader.getPage(0)

    # extract text from page
    textData = pageObj.extractText()

    # close pdf file object
    pdfFileObj.close()
    print(textData)
    return textData