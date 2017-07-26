from jinja2_htmltemplate.template import Template
from nose.tools import eq_


def test_jinja_template():
    t = Template('<title><TMPL_VAR NAME="foo"></title>')
    eq_(t.render(foo="Hello World!"), "<title>Hello World!</title>")


def test_jinja_loop():
    t = Template('''
<TMPL_LOOP NAME="loop">
  Item: <TMPL_VAR NAME="item">
  Price: <TMPL_VAR NAME="price">
  ---
</TMPL_LOOP>
''')
    out = '''

  Item: item 1
  Price: 1000
  ---

  Item: item 2
  Price: 2000
  ---
'''
    eq_(t.render(
            loop=[
                {"item": "item 1", "price": 1000},
                {"item": 'item 2', "price": 2000}
            ]),
        out,
        msg='loop')
