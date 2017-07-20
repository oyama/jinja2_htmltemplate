jinja2_htmltemplate
~~~~~~~~~~~~~~~~~~~

jinja2_htmltemplate is a meta-template engine written in pure Python.
It provides a translate from Perl HTML::Template template to Python Jinja2 template.

Nutshell
--------
Here a small example:

.. code-block:: python

    from jinja2_htmltemplate.translate import HtmlTemplate

    print(HtmlTemplate().from_string('''
        <title><TMPL_VAR NAME="title"><title>
        <ul>
        <TMPL_LOOP NAME="users">
            <li><a href="<TMPL_VAR NAME="url">"><TMPL_VAR NAME="username"></a></li>
        </TMPL_LOOP>
        </ul>'''))

This code outputs the following Jinja2 template:

.. code-block:: jinja

        <title>{{ title }}<title>
        <ul>
        {% for _for_object_users in users %}
            <li><a href="{{ _for_object_users.url }}">{{ _for_object_users.username }}</a></li>
        {% endfor %}
        </ul>

Builds
------
.. code-block:: bash

git clone git@github.com:oyama/jinja2_htmltemplate src/github.com/oyama/jinja2_htmltemplate
src/github.com/oyama/jinja2_htmltemplate
docker build -t jinja2_htmltemplate .
docker run --rm -it -v $(pwd):/root/jinja2_htmltemplate -w /root/jinja2_htmltemplate jinja2_htmltemplate python setup.py nosetests
