import logging
import sys
import time
from datetime import datetime

import requests

from conf import Config
from utils import BitcoinNode, DatabaseConnection


class BitcoinNodeSyncChecker(object):
    def __init__(self):
        self.logger = logging.getLogger('checker_logger')
        self.logger.setLevel(logging.INFO)

        self.bitcoin_node = BitcoinNode()
        self.database_connection = DatabaseConnection()

        if not self.database_connection.is_established_connection:
            self.logger.error('No connection with database')
            sys.exit(1)

    def get_latest_block_info(self):
        response = requests.get('https://blockchain.info/latestblock')
        if response.status_code != 200:
            self.logger.error('Connection refused from {}'.format(response.url))
            sys.exit(1)
        data = response.json()

        return data

    @property
    def latest_block_blocks_count(self):
        latest_block_info = self.get_latest_block_info()
        return latest_block_info['height']

    @property
    def node_blocks_count(self):
        try:
            blocks_count = self.bitcoin_node.node_connection.getblockcount()
            return blocks_count
        except ConnectionError:
            self.logger.error('Connection refused from bitcoin node')
            sys.exit(1)

    @property
    def delta_origin_and_node_blocks(self):
        return int(self.latest_block_blocks_count) - int(self.node_blocks_count)

    def save_check_result(self):
        json_data = [
            {
                "measurement": Config.CHECKER_MEASUREMENT_NAME,
                "time": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    "value": self.node_blocks_count,
                    "delta": self.delta_origin_and_node_blocks,
                }
            }
        ]

        self.database_connection.client.write_points(json_data)

    def run(self):
        starttime = time.time()
        while True:
            self.save_check_result()
            time.sleep(Config.CALL_TIMEOUT - ((time.time() - starttime) % Config.CALL_TIMEOUT))


if __name__ == '__main__':
    checker = BitcoinNodeSyncChecker()
    checker.run()
