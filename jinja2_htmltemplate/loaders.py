import jinja2.loaders as jinja2_loaders
from jinja2_htmltemplate.translate import HtmlTemplate


class FileSystemLoader(jinja2_loaders.FileSystemLoader):
    def get_source(self, environment, template):
        source, filename, uptodate = super().get_source(environment, template)
        return HtmlTemplate().from_string(source), filename, uptodate
