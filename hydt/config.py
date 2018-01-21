import os
from pathlib import Path

home = str(Path.home())
HERE = os.path.dirname(__file__)
APP = os.path.join(HERE, '..')


class Config:
    """super simple configuration object"""
    options = {}

    def __init__(self, **options):
        self.fill(**options)

    def fill(self, **options):
        options = options or {}

        for k, v in options.items():
            self.options[k] = v

    def __getattr__(self, attr):
        return self.options.get(attr, None)

    def __setattr__(self, attr, value):
        self.options[attr] = value


options = Config()
options.db_location = os.path.join(home, 'hydt.db')
options.template_path = os.path.join(HERE, 'template')
options.report_save_directory = os.path.join(home, 'hydt', 'reports')
options.host_name = 'http://energy.datcode.io'
