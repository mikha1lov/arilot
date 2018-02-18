import http.client as httplib
import ssl
import urllib.parse as urlparse

from bitcoinrpc.authproxy import HTTP_TIMEOUT, AuthServiceProxy
from influxdb import InfluxDBClient

from conf import Config


class BitcoinNode(object):

    def __init__(self):
        self._base_host = Config.RPC_HOST
        self._port = Config.RPC_PORT
        self._username = Config.RPC_USER
        self._password = Config.RPC_PASSWORD
        self._check_ssl = Config.RPC_CHECK_SSL

        self.host = urlparse.urlparse(self._base_host)

        self.node_url = '{scheme}://{user}:{password}@{host_name}:{port}'.format(
            scheme=self.host.scheme,
            user=self._username,
            password=self._password,
            host_name=self.host.hostname,
            port=self._port
        )

        self.node_connection = self.get_node_connection()

    def _get_no_ssl_connection_context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def _get_connection(self):
        connection = None
        if not self._check_ssl and self.host.scheme == 'https':
            context = self._get_no_ssl_connection_context()
            connection = httplib.HTTPSConnection(self.host.hostname, self._port,
                                                 timeout=HTTP_TIMEOUT, context=context)
        return connection

    def get_node_connection(self):
        connection = self._get_connection()
        return AuthServiceProxy(self.node_url, connection=connection)


class DatabaseConnection(object):
    def __init__(self):
        self.client = InfluxDBClient(
            host=Config.NFLUXDB_HOST,
            port=Config.PORT,
            database=Config.DATABASE_NAME
        )

    @property
    def is_established_connection(self):
        try:
            self.client.ping()
            return True
        except:
            return False
