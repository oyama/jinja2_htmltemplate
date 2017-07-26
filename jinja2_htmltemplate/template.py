import jinja2

from jinja2_htmltemplate.translate import HtmlTemplate


class Template(jinja2.Template):
    def __new__(cls, html_template):
        source = HtmlTemplate().from_string(html_template)
        return super().__new__(cls, source)
