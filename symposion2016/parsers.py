from symposion.markdown_parser import parse


class MarkdownHookSet(object):

    def parse_content(self, content):
        return parse(content)
