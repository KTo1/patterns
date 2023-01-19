import os
from jinja2 import Environment, FileSystemLoader

from savraska.request import Request


class Engine:

    def __init__(self, base_dir: str, template_dir: str, static_dir_name: str):
        self.template_dir = template_dir
        self.full_template_dir = os.path.join(base_dir, template_dir)
        self.static_url = f'/{static_dir_name}/'

    def as_string(self, template_name: str):
        template_path = os.path.join(self.full_template_dir, template_name)

        if not os.path.isfile(template_path):
            raise Exception(f'{template_name} is not file')

        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def build(self, context: dict, template_name: str) -> str:
        template = Environment(loader=FileSystemLoader(self.template_dir)).from_string(self.as_string(template_name))
        template.globals['static'] = self.static_url
        return template.render(**context)


def build_template(request: Request, context: dict, template_name: str) -> str:
    assert request.settings.get('BASE_DIR')
    assert request.settings.get('TEMPLATES_DIR_NAME')
    assert request.settings.get('STATIC_DIR')

    base_dir = request.settings.get('BASE_DIR')
    template_dir_name = request.settings.get('TEMPLATES_DIR_NAME')
    static_dir_name = request.settings.get('STATIC_DIR_NAME')

    engine = Engine(base_dir, template_dir_name, static_dir_name)

    return engine.build(context, template_name)