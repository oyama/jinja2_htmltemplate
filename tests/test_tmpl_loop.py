from jinja2_htmltemplate.translate import HtmlTemplate
from nose.tools import ok_, eq_


def test_simple_loop():
    t = HtmlTemplate()
    perl = (
        '<TMPL_LOOP NAME="loop">'
        '  Name: <TMPL_VAR NAME="name">'
        '  Price: <TMPL_VAR NAME="price">'
        '</TMPL_LOOP>')
    python = (
        '{% for _for_object_loop in loop %}'
        '  Name: {{ _for_object_loop.name }}'
        '  Price: {{ _for_object_loop.price }}'
        '{% endfor %}')
    eq_(t.from_string(perl), python, msg='simple TMPL_LOOP')


def test_nested_loop():
    t = HtmlTemplate()
    perl = (
        '<TMPL_LOOP NAME="loop">'
        '  Name: <TMPL_VAR NAME="name">'
        '  Price: <TMPL_VAR NAME="price">'
        '  Tags: <TMPL_LOOP NAME="tags"> <TMPL_VAR NAME="tag"></TMPL_LOOP>'
        '</TMPL_LOOP>')
    python = (
        '{% for _for_object_loop in loop %}'
        '  Name: {{ _for_object_loop.name }}'
        '  Price: {{ _for_object_loop.price }}'
        '  Tags: {% for _for_object_tags in _for_object_loop.tags %}'
        ' {{ _for_object_tags.tag }}{% endfor %}'
        '{% endfor %}')
    eq_(t.from_string(perl), python, msg='nested TMPL_LOOP')
