FROM python:3.6

ADD jinja2_htmltemplate /root/jinja2_htmltemplate
RUN pip install jinja2 nose coverage
