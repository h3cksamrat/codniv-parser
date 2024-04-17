from unittest import TestCase

from parser.parser import parse_pdf


class TestMain(TestCase):
    def test_pdf_with_no_tables(self):
        tables = parse_pdf("./pdfs/pdf1.pdf")
        self.assertEqual(len(tables), 0)

    def test_pdf_with_single_table(self):
        tables = parse_pdf("./pdfs/pdf4.pdf")
        self.assertEqual(len(tables), 1)

    def test_pdf_with_password(self):
        tables = parse_pdf("./pdfs/pdf5.pdf", password="123456")
        self.assertTrue(len(tables), 1)

    def test_pdf_with_more_tables(self):
        tables = parse_pdf("./pdfs/pdf2.pdf")
        self.assertEqual(len(tables), 5)

    def test_pdf_with_false_tables_too(self):
        tables = parse_pdf("./pdfs/pdf3.pdf")
        self.assertEqual(len(tables), 10)
