#!/usr/bin/env python

import json
import os
import logging
import sqlite3
import time
import oandapy
import pandas as pd
import pandas.io.sql as pdsql
from ..util.config import read_config_yml


def track_rate(config_yml, instruments, granularity, count, csv_path=None,
               sqlite_path=None, print_json=False, quiet=False):
    logger = logging.getLogger(__name__)
    logger.info('Rate tracking')
    cf = read_config_yml(path=config_yml)
    oanda = oandapy.API(
        environment=cf['oanda']['environment'],
        access_token=cf['oanda']['access_token']
    )
    candles = dict()
    for i in (instruments or cf['instruments']):
        candles[i] = [
            d for d in oanda.get_history(
                account_id=cf['oanda']['account_id'], instrument=i,
                candleFormat='bidask', granularity=granularity,
                count=int(count)
            )['candles'] if d['complete']
        ]
        time.sleep(0.5)
    keys = ['instrument', 'time']
    df_all = pd.concat([
        pd.DataFrame(c).assign(instrument=i) for i, c in candles.items()
    ]).drop(columns=['complete']).set_index(keys)
    if sqlite_path:
        logger.debug('df_all.shape: {}'.format(df_all.shape))
        sqlite_abspath = os.path.abspath(
            os.path.expanduser(os.path.expandvars(sqlite_path))
        )
        if os.path.isfile(sqlite_abspath):
            with sqlite3.connect(sqlite_abspath) as con:
                df_db_diff = df_all.join(
                    pdsql.read_sql(
                        'SELECT instrument, time FROM candle;', con
                    ).assign(
                        in_db=True
                    ).set_index(keys),
                    on=keys, how='left'
                ).pipe(
                    lambda d: d[d['in_db'].isnull()].drop(columns=['in_db'])
                )
                logger.debug(
                    'df_db_diff:{0}{1}'.format(os.linesep, df_db_diff)
                )
                pdsql.to_sql(df_db_diff, 'candle', con, if_exists='append')
        else:
            schema_sql_path = os.path.join(
                os.path.dirname(__file__), '../static/create_tables.sql'
            )
            with open(schema_sql_path, 'r') as f:
                schema_sql = f.read()
            with sqlite3.connect(sqlite_abspath) as con:
                con.executescript(schema_sql)
                logger.debug('df_all:{0}{1}'.format(os.linesep, df_all))
                pdsql.to_sql(df_all, 'candle', con, if_exists='append')
    if csv_path:
        csv_abspath = os.path.abspath(
            os.path.expanduser(os.path.expandvars(csv_path))
        )
        sep = (',' if csv_abspath.endswith('.csv') else '\t')
        if os.path.isfile(csv_abspath):
            if csv_abspath.endswith('.csv'):
                df_prev = pd.read_csv(csv_abspath)[keys]
            else:
                df_prev = pd.read_table(csv_abspath)[keys]
            df_csv_diff = df_all.join(
                df_prev.assign(in_csv=True).set_index(keys),
                on=keys, how='left'
            ).pipe(
                lambda d: d[d['in_csv'].isnull()].drop(columns=['in_csv'])
            )
            df_csv_diff.to_csv(csv_abspath, mode='a', header=False, sep=sep)
        else:
            df_all.to_csv(csv_abspath, mode='w', header=True, sep=sep)
    if not quiet:
        if print_json:
            print(json.dumps(candles, indent=2))
        else:
            with pd.option_context('display.max_rows', None):
                print(df_all)
