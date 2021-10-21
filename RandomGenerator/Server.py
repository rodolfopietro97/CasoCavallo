import redis


from Utils.CasoCavalloConstants import REDIS_SERVER, CONFIGURATION_FILE_PATH
from Utils.ConfigurationFiles.CasoCavalloConfigurationFileHandler import CasoCavalloConfigurationFileHandler
from Workers.ServerWorker import server_worker
from Workers.Viewer import viewer_worker

import time

if __name__ == '__main__':
    """
    Main method
    """
    try:
        # Init redis client
        redis_client = redis.Redis(
            host=REDIS_SERVER['host'],
            port=REDIS_SERVER['port'],
            db=REDIS_SERVER['database'],
            socket_timeout=REDIS_SERVER['connection_timeout']
        )

        # Load all queues from configuration file
        redis_queues = CasoCavalloConfigurationFileHandler \
            .load_queues_from_configuration_file(CONFIGURATION_FILE_PATH)

        # Get redis lists from queues
        redis_lists = [redis_queue['name'] for redis_queue in redis_queues]

        # Viewer process. It is for report functionality
        while True:
            server_worker(redis_client=redis_client, redis_lists=redis_lists, cummare_clients_path="../../Cummare/dist/", picinusu_fetcher_path="../../Picinusu/fetchRandomRequestsAndResolveResponses.py", cummare_server="127.0.0.1:50052")
            time.sleep(1)

    except Exception as exception:
        print(f"Error on init Redis\n{exception}")
