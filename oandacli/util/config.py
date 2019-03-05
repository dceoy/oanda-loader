#!/usr/bin/env python

import logging
import os
import shutil
import v20
import yaml


def read_yml(path):
    with open(path, 'r') as f:
        d = yaml.load(f)
    return d


def write_config_yml(path):
    logger = logging.getLogger(__name__)
    if os.path.exists(path):
        print('A file already exists: {}'.format(path))
    else:
        logger.info('Write a config: {}'.format(path))
        shutil.copyfile(
            os.path.join(
                os.path.dirname(__file__), '../static/default_oanda.yml'
            ),
            path
        )
        print('A YAML template was generated: {}'.format(path))


def fetch_config_yml_path(path=None, env='OANDA_YML', default='oanda.yml'):
    logger = logging.getLogger(__name__)
    p = [
        os.path.abspath(os.path.expanduser(os.path.expandvars(p)))
        for p in [path, os.getenv(env), default] if p is not None
    ][0]
    logger.debug('abspath to a config: {}'.format(p))
    return p


def create_api(config):
    return v20.Context(
        hostname=config['oanda']['hostname'], port=config['oanda']['port'],
        ssl=config['oanda']['ssl'], application='oandacli',
        token=config['oanda']['token'], decimal_number_as_float=True,
        stream_chunk_size=512, stream_timeout=10, datetime_format='RFC3339',
        poll_timeout=2
    )
