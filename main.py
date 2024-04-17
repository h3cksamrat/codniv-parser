
from parser.parser import parse_pdf


if __name__ == "__main__":
    pdfs = [
        {"path": "pdfs/pdf1.pdf", "password": None},
        {"path": "pdfs/pdf2.pdf", "password": None},
        {"path": "pdfs/pdf3.pdf", "password": None},
        {"path": "pdfs/pdf4.pdf", "password": None},
        {"path": "pdfs/pdf5.pdf", "password": "123456"},
    ]

    for pdf in pdfs:
        parse_pdf(pdf["path"], pdf["password"])
