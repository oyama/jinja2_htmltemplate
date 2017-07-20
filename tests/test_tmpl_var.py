from nose.tools import eq_
from jinja2_htmltemplate.translate import HtmlTemplate


def test_tmpl_var():
    t = HtmlTemplate()
    eq_('{{ foo }}',          t.from_string('<TMPL_VAR NAME="foo">'), msg='TMPL_VAR')
    eq_('Subject:{{ foo }}',  t.from_string('Subject:<TMPL_VAR NAME="foo">'), msg='prefix')
    eq_('{{ foo }}<br />',    t.from_string('<TMPL_VAR NAME="foo"><br />'), msg='suffix')
    eq_('{{ foo }}{{ bar }}', t.from_string('<TMPL_VAR NAME="foo"><TMPL_VAR NAME="bar">'), msg='repeat')


def test_escape():
    t = HtmlTemplate()
    eq_(t.from_string('<TMPL_VAR NAME="foo" ESCAPE="html">'), '{{ foo|e }}', msg='TMPL_VAR escape html')
    eq_(t.from_string('<TMPL_VAR NAME="foo" ESCAPE="1">'),    '{{ foo|e }}', msg='TMPL_VAR old escape html')
    eq_(t.from_string('<TMPL_VAR NAME="foo" ESCAPE="url">'),  '{{ foo|urlencode }}', msg='TMPL_VAR escape url')
    eq_(t.from_string('<TMPL_VAR NAME="foo" ESCAPE="js">'),   '{{ foo|tojson }}',    msg='TMPL_VAR escape json')
    eq_(t.from_string('<TMPL_VAR NAME="foo" ESCAPE="none">'), '{{ foo }}', msg='TMPL_VAR escape none')


def test_default():
    t = HtmlTemplate()
    eq_(t.from_string('<TMPL_VAR NAME="foo" DEFAULT="Hello World!">'), "{{ foo|default('Hello World!') }}")
    eq_(t.from_string('<TMPL_VAR NAME="foo" DEFAULT="Hello\'world">'), "{{ foo|default('Hello\'world') }}", msg='escape single quote')

    eq_("{{ foo|default('Hello World!')|e }}", t.from_string('<TMPL_VAR NAME="foo" ESCAPE="html" DEFAULT="Hello World!">'), msg='TMPL_VAR escape and default')
