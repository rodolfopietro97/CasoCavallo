from multiprocessing import Process

import redis

from Utils.ConfigurationFiles.CasoCavalloConfigurationFileHandler import CasoCavalloConfigurationFileHandler
from Utils.CasoCavalloConstants import \
    CONFIGURATION_FILE_PATH
from Workers.Generator import generator_worker
from Workers.Merger import merger_worker
from Workers.Remover import remover_worker
from Workers.Viewer import viewer_worker
from Workers.PerformanceTester import performance_tester_worker

import sys

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
        redis_server = CasoCavalloConfigurationFileHandler.load_redis_server_from_configuration_file(CONFIGURATION_FILE_PATH)
        redis_client = redis.Redis(
            host=redis_server['host'],
            port=redis_server['port'],
            db=redis_server['database'],
            socket_timeout=redis_server['connection_timeout']
        )

        # Load all redis queues from configuration file
        redis_queues = CasoCavalloConfigurationFileHandler \
            .load_queues_from_configuration_file(CONFIGURATION_FILE_PATH)

        # Get redis lists names from our redis queues
        redis_lists = [redis_queue['name'] for redis_queue in redis_queues]

        # Delete all previous redis lists
        for redis_list in redis_lists:
            if redis_client.exists(redis_list):
                redis_client.delete(redis_list)

        # Run test of properties
        # TODO improve with a logging system
        if CasoCavalloConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "doInitialPerformancesTest"):
            performance_tester_worker(random_sources=random_sources)

        # 3) ***** Start a process for each random source and for each queue *****
        # For each random source
        for random_source in random_sources:
            generator = Process(target=generator_worker, args=(redis_client, random_source, redis_queues,))
            remover = Process(target=remover_worker, args=(redis_client, redis_lists,))
            merger = Process(target=merger_worker, args=(redis_client, redis_queues))

            generator.start()
            remover.start()
            merger.start()

        # 4) Launch Viewer
        if CasoCavalloConfigurationFileHandler.get_generic_property(CONFIGURATION_FILE_PATH, "useViewer"):
            viewer = Process(target=viewer_worker, args=(redis_client, redis_lists))
            viewer.start()

    except Exception as exception:
        print(f"Error on init Redis\n{exception}")
