class Table:
    def __init__(self, title=None, show_header=True, title_style=None):
        self.title = title
        self.rows = []

    def add_row(self, *columns):
        self.rows.append(columns)

    def __str__(self):
        lines = []
        if self.title:
            lines.append(str(self.title))
        for row in self.rows:
            lines.append(' '.join(str(c) for c in row))
        return '\n'.join(lines)
