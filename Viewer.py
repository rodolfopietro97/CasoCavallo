import redis

from Utils.CasoCavalloConstants import CONFIGURATION_FILE_PATH, NEWTORK_CONFIGURATION_FILE_PATH
from Utils.ConfigurationFiles.CasoCavalloConfigurationFileHandler import CasoCavalloConfigurationFileHandler
from Workers.Viewer import viewer_worker

if __name__ == '__main__':
    """
    Main method
    """

    try:
        # Init redis client
        redis_server = CasoCavalloConfigurationFileHandler.load_redis_server_from_configuration_file(NEWTORK_CONFIGURATION_FILE_PATH)
        redis_client = redis.Redis(
            host=redis_server['host'],
            port=redis_server['port'],
            db=redis_server['database'],
            socket_timeout=redis_server['connection_timeout']
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
