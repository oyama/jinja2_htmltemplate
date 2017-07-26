from jinja2 import Environment
from jinja2_htmltemplate.loaders import FileSystemLoader
from nose.tools import eq_


def test_include():
    env = Environment(loader=FileSystemLoader('tests/res'))
    t = env.get_template('templates/include_base.html')
    out = t.render(title='Hello, Include!', message='Hello World!')
    eq_('<html><head><title>Hello, Include!</title></head>'
        '<body><h1>Hello World!</h1></body></html>',
        out)
