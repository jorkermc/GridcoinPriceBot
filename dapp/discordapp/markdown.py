class CodeBlock:
    def __init__(self, text, code_type=''):
        self.text = text
        self.code_type = code_type

    def __str__(self):
        if '\n' in self.text:
            return '```{}\n'.format(self.code_type) + self.text + '\n```'
        return '`' + self.text + '`'
