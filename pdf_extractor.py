from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from block import Block
import pdf2image


class PdfExtractor:
    def __parse_layout(self, layout, pages, w, h):
        for lt_obj in layout:
            x1, y1, x2, y2 = lt_obj.bbox
            text = 'Object ' + lt_obj.__class__.__name__
            pages.append(Block(x1 / w, 1 - y2 / h, x2 / w, 1 - y1 / h, text))

            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                pages[-1].text = lt_obj.get_text()
            elif isinstance(lt_obj, LTFigure):
                self.__parse_layout(lt_obj, pages, w, h)

    def __extract_pages(self, doc: PDFDocument):
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        pages = []

        for i, page in enumerate(PDFPage.create_pages(doc)):
            interpreter.process_page(page)
            layout = device.get_result()
            x, y, w, h = page.mediabox
            page = []
            self.__parse_layout(layout, page, w, h)
            pages.append(page)

        return pages

    def extract(self, path: str, dpi=70):
        fp = open(path, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)

        images = pdf2image.convert_from_path(path, dpi)
        pages = self.__extract_pages(doc)

        return images, pages
