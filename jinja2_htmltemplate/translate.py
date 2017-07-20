import re
import enum

class Tokens(enum.IntFlag):
    TEXT            = 1
    TMPL_VAR        = 2
    TMPL_LOOP       = 3
    TMPL_LOOP_END   = 4
    TMPL_INCLUDE    = 5
    TMPL_IF         = 6
    TMPL_IF_END     = 7
    TMPL_ELSE       = 8
    TMPL_UNLESS     = 9
    TMPL_UNLESS_END = 10
    UNKNOWN         = 11

class TokenIndex(enum.IntFlag):
    TYPE    = 0
    TEXT    = 1
    NAME    = 2
    ESCAPE  = 3
    DEFAULT = 4


class HtmlTemplate(object):
    def from_string(self, source):
        tokens = self.tokenize(source)
        return self.translate(tokens)

    def tokenize(self, source):
        tokenizer = re.compile("(?:<(?:TMPL_VAR|TMPL_LOOP|TMPL_INCLUDE|TMPL_IF|TMPL_ELSE|TMPL_UNLESS)(?:\s+[^>]+)?>|</(?:TMPL_VAR|TMPL_LOOP|TMPL_INCLUDE|TMPL_IF|TMPL_ELSE|TMPL_UNLESS)>|.+?)", flags=re.DOTALL)
        tokens = []
        buffer = []
        for line in source.splitlines(keepends=True):
            for m in tokenizer.finditer(line):
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
        texts = []
        stack = []
        for token in tokens:
            if token[TokenIndex.TYPE] == Tokens.TEXT:
                texts.append(token[TokenIndex.TEXT])
            elif token[TokenIndex.TYPE] == Tokens.TMPL_VAR:
                name = token[TokenIndex.NAME]
                if len(stack) > 0:
                    name = "{stack}.{name}".format(stack = stack[len(stack)-1], name = name)

                default_filter = ''
                if token[TokenIndex.DEFAULT] != None:
                    default_filter = "|default('{value}')".format(value=token[TokenIndex.DEFAULT].replace("'", "\'"))

                escape_filter = ''
                if token[TokenIndex.ESCAPE] == 'html' or token[TokenIndex.ESCAPE] == '1':
                    escape_filter = '|e'
                elif token[TokenIndex.ESCAPE] == 'js':
                    escape_filter = '|tojson'
                elif token[TokenIndex.ESCAPE] == 'url':
                    escape_filter = '|urlencode'
                elif token[TokenIndex.ESCAPE] == 'none':
                    escape_filter = ''
                else:
                    escape_filter = ''
                texts.append('{{ ' + name + default_filter + escape_filter + ' }}')
            elif token[TokenIndex.TYPE] == Tokens.TMPL_LOOP:
                name = token[TokenIndex.NAME]
                if len(stack) > 0:
                    name = "{stack}.{name}".format(stack= stack[len(stack)-1], name = name)
                i = "_for_object_{name}".format(name=token[TokenIndex.NAME])
                texts.append('{%' + " for {i} in {name} ".format(name = name, i = i) + '%}')
                stack.append(i)
            elif token[TokenIndex.TYPE] == Tokens.TMPL_LOOP_END:
                texts.append("{% endfor %}")
                stack.pop()
            elif token[TokenIndex.TYPE] == Tokens.TMPL_IF:
                texts.append('{% if ' + token[TokenIndex.NAME] +  ' %}')
            elif token[TokenIndex.TYPE] == Tokens.TMPL_IF_END:
                texts.append("{% endif %}")
            elif token[TokenIndex.TYPE] == Tokens.TMPL_ELSE:
                texts.append("{% else %}")
            elif token[TokenIndex.TYPE] == Tokens.TMPL_UNLESS:
                texts.append('{% if not ' + token[TokenIndex.NAME] +  ' %}')
            elif token[TokenIndex.TYPE] == Tokens.TMPL_UNLESS_END:
                texts.append("{% endif %}")
 
        return "".join(texts)


    def _parse_tmpl_token(self, token):
        tmpl_tokenizer = re.compile("<(/)?(TMPL_VAR|TMPL_LOOP|TMPL_INCLUDE|TMPL_IF|TMPL_ELSE|TMPL_UNLESS)\s*([^>]+)?>")

        m = tmpl_tokenizer.match(token)
        if not m:
            return (Tokens.UNKNOWN, token)
        if m.group(2) == 'TMPL_VAR':
            attr = m.group(3)
            return (Tokens.TMPL_VAR, token, self._get_name(attr), self._get_escape(attr), self._get_default(attr))
        elif m.group(2) == 'TMPL_LOOP' and m.group(1) == None:
            return (Tokens.TMPL_LOOP, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_LOOP' and m.group(1) == '/':
            return (Tokens.TMPL_LOOP_END, token)
        elif m.group(2) == 'TMPL_INCLUDE':
            return (Tokens.TMPL_INCLUDE, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_IF' and m.group(1) == None:
            return (Tokens.TMPL_IF, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_IF' and m.group(1) == '/':
            return (Tokens.TMPL_IF_END, token)
        elif m.group(2) == 'TMPL_ELSE':
            return (Tokens.TMPL_ELSE, token)
        elif m.group(2) == 'TMPL_UNLESS' and m.group(1) == None:
            return (Tokens.TMPL_UNLESS, token, self._get_name(m.group(3)))
        elif m.group(2) == 'TMPL_UNLESS' and m.group(1) == '/':
            return (Tokens.TMPL_UNLESS_END, token)
        else:
            return (Tokens.UNKNOWN, token)


    def _get_name(self, options):
        m = re.search(r"NAME=(?:[\"'])?([0-9A-Za-z/\+\-_.]+)(?:[\"'])?", options)
        if not m:
            return None
        return m.group(1)


    def _get_escape(self, attributes):
        m = re.search(r"ESCAPE=(?:[\"'])?(1|html|js|url|none)(?:[\"'])?", attributes)
        if not m:
            return None
        return m.group(1)


    def _get_default(self, attributes):
        m = re.search(r'DEFAULT=\"([^"]+)"', attributes)
        if not m:
            return None
        return m.group(1)



#h2j = HtmlTemplate("perl.tmpl")
#h2j._get_source()
