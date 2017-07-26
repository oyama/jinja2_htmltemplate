from setuptools import setup, find_packages

setup(
    name="jinja2_htmltemplate",
    version="0.0.1",
    packages=find_packages(),
    install_requires=['nose', 'jinja2'],

    author="Hiroyuki OYAMA",
    author_email="oyama@module.jp",
    description=("Translate from Perl HTML::Template template to "
                 "Python Jinja2 template"),
    license="PSF",
    keywords="perl jinja template convert",
    url="https://github.com/oyama/jinja2_htmltemplate",
)
