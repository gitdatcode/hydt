import os

from .opitons import options


HERE = os.path.dirname(__file__)
APP = os.path.join(HERE, '..')


options.db_location = os.path.join(HERE, 'model', 'hydt.db')
