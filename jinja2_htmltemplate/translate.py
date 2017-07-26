import enum
import re


class Tokens(enum.IntFlag):
    TEXT = 1
    TMPL_VAR = 2
    TMPL_LOOP = 3
    TMPL_LOOP_END = 4
    TMPL_INCLUDE = 5
    TMPL_IF = 6
    TMPL_IF_END = 7
    TMPL_ELSE = 8
    TMPL_UNLESS = 9
    TMPL_UNLESS_END = 10
    UNKNOWN = 11


class TokenIndex(enum.IntFlag):
    TYPE = 0
    TEXT = 1
    NAME = 2
    ESCAPE = 3
    DEFAULT = 4


html_template_tokenizer_re = re.compile(
    r"(?:"
    r"<(?:TMPL_VAR|TMPL_LOOP|TMPL_INCLUDE|TMPL_IF|TMPL_ELSE|TMPL_UNLESS)"
    r"(?:\s+[^>]+)?>"
    r"|"
    r"</(?:TMPL_VAR|TMPL_LOOP|TMPL_INCLUDE|TMPL_IF|TMPL_ELSE|TMPL_UNLESS)>"
    r"|.+?"
    r")",
    flags=re.DOTALL)

tmpl_token_re = re.compile(
    r"<(/)?"
    r"(TMPL_VAR|TMPL_LOOP|TMPL_INCLUDE|TMPL_IF|TMPL_ELSE|TMPL_UNLESS)"
    r"\s*([^>]+)?"
    r">")


class HtmlTemplate(object):

    def from_string(self, source):
        tokens = self.tokenize(source)
        return self.translate(tokens)

    def tokenize(self, source):
        tokens = []
        buffer = []
        for line in source.splitlines(keepends=True):
            for m in html_template_tokenizer_re.finditer(line):
                token = m.group()
                if len(token) == 1:
                    buffer.append(token)
                    continue
                else:
                    text_token = "".join(buffer)
                    buffer.clear()
                    tokens.append((Tokens.TEXT, text_token))
                tmpl_token = token
                tokens.append(self._parse_tmpl_token(tmpl_token))

        if len(buffer) > 0:
            text_token = "".join(buffer)
            buffer.clear()
            tokens.append((Tokens.TEXT, text_token))
        return tokens

    def translate(self, tokens):
        handler = TokenHandler()
        for token in tokens:
            if token[TokenIndex.TYPE] == Tokens.TEXT:
                handler.text(token[TokenIndex.TEXT])
            elif token[TokenIndex.TYPE] == Tokens.TMPL_VAR:
                handler.tmpl_var(token[TokenIndex.NAME],
                                 token[TokenIndex.ESCAPE],
                                 token[TokenIndex.DEFAULT])
            elif token[TokenIndex.TYPE] == Tokens.TMPL_LOOP:
                handler.tmpl_loop(token[TokenIndex.NAME])
            elif token[TokenIndex.TYPE] == Tokens.TMPL_LOOP_END:
                handler.tmpl_loop_end()
            elif token[TokenIndex.TYPE] == Tokens.TMPL_INCLUDE:
                handler.tmpl_include(token[TokenIndex.NAME])
            elif token[TokenIndex.TYPE] == Tokens.TMPL_IF:
                handler.tmpl_if(token[TokenIndex.NAME])
            elif token[TokenIndex.TYPE] == Tokens.TMPL_IF_END:
                handler.tmpl_if_end()
            elif token[TokenIndex.TYPE] == Tokens.TMPL_ELSE:
                handler.tmpl_else()
            elif token[TokenIndex.TYPE] == Tokens.TMPL_UNLESS:
                handler.tmpl_unless(token[TokenIndex.NAME])
            elif token[TokenIndex.TYPE] == Tokens.TMPL_UNLESS_END:
                handler.tmpl_unless_end()
            else:
                handler.tmpl_unknown(token[TokenIndex.TEXT])
        return handler.get_template()

    def _parse_tmpl_token(self, token):
        m = tmpl_token_re.match(token)
        if not m:
            return (Tokens.UNKNOWN, token)
        if m.group(2) == 'TMPL_VAR':
            attr = m.group(3)
            return (Tokens.TMPL_VAR,
                    token,
                    self._get_name(attr),
                    self._get_escape(attr), self._get_default(attr))
        elif m.group(2) == 'TMPL_LOOP' and m.group(1) is None:
            return (Tokens.TMPL_LOOP, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_LOOP' and m.group(1) == '/':
            return (Tokens.TMPL_LOOP_END, token)
        elif m.group(2) == 'TMPL_INCLUDE':
            return (Tokens.TMPL_INCLUDE, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_IF' and m.group(1) is None:
            return (Tokens.TMPL_IF, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_IF' and m.group(1) == '/':
            return (Tokens.TMPL_IF_END, token)
        elif m.group(2) == 'TMPL_ELSE':
            return (Tokens.TMPL_ELSE, token)
        elif m.group(2) == 'TMPL_UNLESS' and m.group(1) is None:
            return (Tokens.TMPL_UNLESS, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_UNLESS' and m.group(1) == '/':
            return (Tokens.TMPL_UNLESS_END, token)
        else:
            return (Tokens.UNKNOWN, token)

    def _get_name(self, options):
        m = re.search(r"NAME=(?:[\"'])?([0-9A-Za-z/\+\-_.]+)(?:[\"'])?",
                      options)
        if not m:
            return None
        return m.group(1)

    def _get_escape(self, attributes):
        m = re.search(r"ESCAPE=(?:[\"'])?(1|html|js|url|none)(?:[\"'])?",
                      attributes)
        if not m:
            return None
        return m.group(1)

    def _get_default(self, attributes):
        m = re.search(r'DEFAULT=\"([^"]+)"', attributes)
        if not m:
            return None
        return m.group(1)


class TokenHandler(object):
    def __init__(self):
        self.stack = []
        self.buffer = []

    def get_template(self):
        return "".join(self.buffer)

    def append(self, token):
        self.buffer.append(token)

    def text(self, token):
        self.append(token)

    def tmpl_var(self, name, escape, default):
        if len(self.stack) > 0:
            last = len(self.stack) - 1
            name = "{stack}.{name}".format(stack=self.stack[last], name=name)

        default_filter = ''
        if default is not None:
            escaped_value = default.replace("'", "\'")
            default_filter = "|default('{value}')".format(value=escaped_value)

        escape_filter = ''
        if escape == 'html' or escape == '1':
            escape_filter = '|e'
        elif escape == 'js':
            escape_filter = '|tojson'
        elif escape == 'url':
            escape_filter = '|urlencode'
        elif escape == 'none':
            escape_filter = ''
        else:
            escape_filter = ''
        self.append('{{ ' + name + default_filter + escape_filter + ' }}')

    def tmpl_loop(self, name):
        items = name
        if len(self.stack) > 0:
            last = len(self.stack) - 1
            items = "{stack}.{name}".format(stack=self.stack[last], name=name)
        item = "_for_object_{name}".format(name=name)
        self.append("{% "
                    + "for {item} in {items}".format(items=items, item=item)
                    + " %}")
        self.stack.append(item)

    def tmpl_loop_end(self):
        self.append("{% endfor %}")
        self.stack.pop()

    def tmpl_include(self, name):
        self.append('{% include "' + name + '" %}')

    def tmpl_if(self, name):
        self.append('{% if ' + name + ' %}')

    def tmpl_if_end(self):
        self.append("{% endif %}")

    def tmpl_else(self):
        self.append("{% else %}")

    def tmpl_unless(self, name):
        self.append('{% if not ' + name + ' %}')

    def tmpl_unless_end(self):
        self.append("{% endif %}")

    def tmpl_unknown(self, token):
        # warnings
        self.append(token)
