import redis

from Utils.ConfigurationFiles.CasoCavalloConfigurationFileHandler import CasoCavalloConfigurationFileHandler
from Utils.CasoCavalloConstants import REDIS_SERVER, CONFIGURATION_FILE_PATH
from Workers.Viewer import viewer_worker

if __name__ == '__main__':
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
        viewer_worker(redis_client, redis_lists)

    except Exception as exception:
        print(f"Error on init Redis\n{exception}")
