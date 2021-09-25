import logging
import logging.config
import os
from dotenv import load_dotenv

from .config import ConfigContainer
from .config import initialize as init_config

load_dotenv(os.getenv('CONFIG_ENV'))
container: ConfigContainer = init_config(os.getenv('CONFIG_FILE_PATH', 'config.yaml'), __name__)
logging_config: dict = container.config.get('logging')

if logging_config:
    logging.config.dictConfig(logging_config)
