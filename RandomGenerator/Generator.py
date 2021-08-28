from multiprocessing import Process

import redis

from Utils.ConfigurationFiles.CasoCavalloConfigurationFileHandler import CasoCavalloConfigurationFileHandler
from Utils.CasoCavalloConstants import \
    REDIS_SERVER, \
    CONFIGURATION_FILE_PATH
from Workers.Generator import generator_worker
from Workers.Merger import merger_worker
from Workers.Remover import remover_worker

if __name__ == '__main__':
    """
    Main method
    """

    # ***** 1) Fetch random sources from configuration file *****
    random_sources = CasoCavalloConfigurationFileHandler\
        .load_random_sources_from_configuration_file(CONFIGURATION_FILE_PATH)

    # ***** 2) Init redis and start main loop of generator process *****
    try:
        # Init redis client
        redis_client = redis.Redis(
            host=REDIS_SERVER['host'],
            port=REDIS_SERVER['port'],
            db=REDIS_SERVER['database'],
            socket_timeout=REDIS_SERVER['connection_timeout']
        )

        # Load all redis queues from configuration file
        redis_queues = CasoCavalloConfigurationFileHandler \
            .load_queues_from_configuration_file(CONFIGURATION_FILE_PATH)

        # Get redis lists names from our redis queues
        redis_lists = [redis_queue['name'] for redis_queue in redis_queues]

        # Delete all previous redis lists
        for redis_list in redis_lists:
            redis_client.delete(redis_list)

        # 3) ***** Start a process for each random source and for each queue *****
        # For each random source
        for random_source in random_sources:
            generator = Process(target=generator_worker, args=(redis_client, random_source, redis_queues,))
            remover = Process(target=remover_worker, args=(redis_client, redis_lists,))
            merger = Process(target=merger_worker, args=(redis_client, redis_queues))

            generator.start()
            remover.start()
            merger.start()

    except Exception as exception:
        print(f"Error on init Redis\n{exception}")
