class Block:
    def __init__(self, x1: float, y1: float, x2: float, y2: float, text: str = "<no text>"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.text = text

    def convert_to_js(self):
        text = self.text.replace('\n', '\\n').replace('"', "'")
        return '{{x1: {0}, y1: {1}, x2: {2}, y2: {3}, text: "{4}"}},'.format(self.x1, self.y1, self.x2, self.y2, text)

    def convert_to_html(self, page_id, block_id):
        text = self.text.replace('\n', '<br>')
        return '<div class="viewer-block" onclick="layoutViewer.ScrollTo({0}, {1})">{2}</div>'.format(page_id, block_id, text)