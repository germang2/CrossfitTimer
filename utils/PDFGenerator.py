from fpdf import FPDF


class PDFGenerator(FPDF):

    def __init__(self, pdf_w=210, pdf_h=297, font='Times'):
        super().__init__()
        self.pdf_w = pdf_w
        self.pdf_h = pdf_h
        self.font = font
        # Effective page width, or just epw
        self.epw = self.w - 2 * self.l_margin
        # Set column width to 1/4 of effective page width to distribute content
        # evenly across table and page
        self.col_width = self.epw / 4
        self.set_font(self.font, 'B', 14)
        self.add_page()
        self.cell(self.epw, 0.0, 'Title', align='C')
        self.output('/test.pdf', 'F')

    def update_font(self, font, t='', s=10):
        self.font = font
        self.set_font(self.font, t, s)

    def title(self, text):
        regular_font = self.font
        self.update_font(font='Times', t='B', s=14)
        self.cell(self.epw, 0.0, text, align='C')
        self.update_font(regular_font)
