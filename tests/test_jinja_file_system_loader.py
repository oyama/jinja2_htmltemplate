from jinja2 import Environment
from jinja2.exceptions import TemplateNotFound
from nose.tools import ok_, eq_, raises

from jinja2_htmltemplate.loaders import FileSystemLoader


def test_basic():
    env = Environment(loader=FileSystemLoader('tests/res/templates/'))
    t = env.get_template('filesystem_loader.html')
    ok_(t, msg='FileSystemLoader get_template')
    out = t.render(title='Hello World!',
                   items=[{'name': 'item 1'}, {'name': 'item 2'}])
    eq_(out,
        '''<html>
  <head><title>Hello World!</title></head>
  <body>
    <h1>Hello World!</h1>
    <ol>
      <li>item 1</li><li>item 2</li>
    </ol>
  </body>
</html>''',
        msg='render via FileSystemLoader#1')

    out = t.render(title='HTML::Template FileSystemLoader',
                   items=[{'name': 'Hello World!'}])
    eq_(out,
        '''<html>
  <head><title>HTML::Template FileSystemLoader</title></head>
  <body>
    <h1>HTML::Template FileSystemLoader</h1>
    <ol>
      <li>Hello World!</li>
    </ol>
  </body>
</html>''',
        msg='render via FileSystemLoader#2')


@raises(TemplateNotFound)
def test_nonexistent_templates():
    env = Environment(loader=FileSystemLoader('tests/res/templates/'))
    env.get_template('not_exists.html')
