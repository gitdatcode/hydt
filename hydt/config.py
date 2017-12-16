import os

from tornado.options import define, options


HERE = os.path.dirname(__file__)
APP = os.path.join(HERE, '..')


# check the local environment file to see which environment we're in
try:
    environment = os.path.join(APP, 'environment')

    with open(environment, 'r') as f:
        ENVIRONMENT = f.readline().to_lower().strip()
except Exception as e:
    ENVIRONMENT = 'development'


define('environment', ENVIRONMENT)
define('app_name', 'hydt')
define('port', 9090)

# database
define('db_location', os.path.join(HERE, 'model', 'hydt.db'))

# overwrite the configuration options with a local python file
extra_config = os.path.join(HERE, 'extra.config.py')

if os.path.isfile(extra_config):
    options.parse_config_file(extra_config)
