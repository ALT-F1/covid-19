# -*- coding: utf-8 -*-

import logging
from logging.config import fileConfig
from os import path
logging.getLogger(__name__).addHandler(logging.NullHandler())

fileConfig(path.join(path.dirname(path.abspath(__file__)),
                     'logging_config.ini'))
logger = logging.getLogger()
logger.debug('Start %s', 'dunning services web application')
