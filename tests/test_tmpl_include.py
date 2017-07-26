from nose.tools import eq_
from jinja2_htmltemplate.translate import HtmlTemplate


def test_tmpl_include():
    t = HtmlTemplate()
    out = t.from_string('<TMPL_INCLUDE NAME="foo.html">')
    eq_('{% include "foo.html" %}', out)
