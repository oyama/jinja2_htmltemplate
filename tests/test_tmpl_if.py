from nose.tools import eq_
from jinja2_htmltemplate.translate import HtmlTemplate

def test_tmpl_if():
    t = HtmlTemplate()
    eq_(t.from_string(
        '<TMPL_IF NAME="cond">True</TMPL_IF>'),
        '{% if cond %}True{% endif %}', msg='TMPL_IF')


def test_tmpl_else():
    t = HtmlTemplate()
    eq_(t.from_string(
        '<TMPL_IF NAME="cond">True<TMPL_ELSE>False</TMPL_IF>'),
        '{% if cond %}True{% else %}False{% endif %}', msg='TMPL_IF')
