#!/usr/bin/env python

import logging
import os
import shutil
import yaml


def read_config_yml(path):
    with open(_config_yml_path(path=path)) as f:
        d = yaml.load(f)
    return d


def write_config_yml(path):
    logger = logging.getLogger(__name__)
    p = _config_yml_path(path=path)
    if os.path.exists(p):
        print('A file already exists: {}'.format(p))
    else:
        logger.info('Write a config: {}'.format(p))
        shutil.copyfile(
            os.path.join(
                os.path.dirname(__file__), '../static/default_oanda.yml'
            ),
            _config_yml_path(path=p)
        )
        print('A YAML template was generated: {}'.format(p))


def _config_yml_path(path=None, env='OANDA_YML', default='oanda.yml'):
    logger = logging.getLogger(__name__)
    p = os.path.abspath(os.path.expanduser(
        [p for p in [path, os.getenv(env), default] if p is not None][0]
    ))
    logger.debug('abspath to a config: {}'.format(p))
    return p
