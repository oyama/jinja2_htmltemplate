from nose.tools import eq_
from jinja2_htmltemplate.translate import HtmlTemplate

def test_tmpl_if():
    t = HtmlTemplate()
    eq_(t.from_string(
        '<TMPL_UNLESS NAME="cond">True</TMPL_UNLESS>'),
        '{% if not cond %}True{% endif %}', msg='TMPL_UNLESS')

#def __test_tmpl_else():
    t = HtmlTemplate()
    eq_(t.from_string(
        '<TMPL_UNLESS NAME="cond">False<TMPL_ELSE>True</TMPL_UNLESS>'),
        '{% if not cond %}False{% else %}True{% endif %}', msg='TMPL_UNLESS/ELSE')
