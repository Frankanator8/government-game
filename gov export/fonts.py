import loader

class FontLibrary:
    def __init__(self):
        self.heading = None
        self.body = None

    def load_fonts(self):
        self.heading = (loader.load_font("TitilliumWeb-BoldItalic", 40), 40)
        self.body = (loader.load_font("TitilliumWeb-Regular", 18), 18)