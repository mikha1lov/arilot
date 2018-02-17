import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_env_variable(key):
    try:
        return os.environ[key]
    except KeyError as e:
        logger.error('No environment variable {}'.format(e))
        sys.exit(1)


class Config:
    RPC_HOST = get_env_variable('RPC_HOST')
    RPC_PORT = get_env_variable('RPC_PORT')
    RPC_USER = get_env_variable('RPC_USER')
    RPC_PASSWORD = get_env_variable('RPC_PASSWORD')

    NFLUXDB_HOST = get_env_variable('NFLUXDB_HOST')
    PORT = get_env_variable('PORT')
    DATABASE_NAME = get_env_variable('DATABASE_NAME')

    CHECKER_MEASUREMENT_NAME = 'node_sync'

    CALL_TIMEOUT = int(get_env_variable('CALL_TIMEOUT'))

    CHECK_SSL = os.environ.get('CHECK_SSL', '') == 'TRUE'
