from PySide6.QtGui import QSyntaxHighlighter, QColor, QTextCharFormat, QFont, QTextDocument


def create_text_format(font_color: QColor = QColor('black'),
                       background_color: QColor = None,
                       weight: QFont.Weight = QFont.Weight.Normal) -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setForeground(font_color)
    fmt.setBackground(background_color)
    fmt.setFontWeight(weight)
    return fmt


class SyntaxHighlighter(QSyntaxHighlighter):
    """Higlights text inside QTextDocument which is provided in constructor"""

    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        self.error = create_text_format(QColor('black'), QColor('red').lighter(128), QFont.Weight.Bold)
        self.warn = create_text_format(QColor('black'), QColor('yellow').lighter(128))
        self.isok = create_text_format(QColor('black'), QColor('green').lighter(256))

    def highlightBlock(self, block):
        """Highlights line of text inside QTextDocument based on text occurence"""
        if '[ERROR]' in block:
            self.setFormat(0, len(block), self.error)
        elif '[WARNING]' in block:
            self.setFormat(0, len(block), self.warn)
        elif '[INFO]' in block:
            self.setFormat(0, len(block), self.isok)
