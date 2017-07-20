from setuptools import setup, find_packages

setup(
    name="jinja2_htmltemplate",
    version="0.0.1",
    packages=find_packages(),
    install_requires=['nose', 'jinja2'],
    #test_suite = 'nose.collector',

    author="Hiroyuki OYAMA",
    author_email="oyama@module.jp",
    description="Translate from Perl HTML::Template template to Python Jinja2 template",
    license="PSF",
    keywords="perl jinja template convert",
    url="https://github.com/find-job/jinja2_htmltemplate",
)
