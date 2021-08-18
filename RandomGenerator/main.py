from time import sleep

from RandomSources.Internal.ClassicalRandomRandomSource import ClassicalRandomRandomSource
from RandomSources.Internal.DevUrandomRandomSource import DevUrandomRandomSource
import redis
import sys
from multiprocessing import Process

from Utils.CasoCavalloConfigurationFileHandler import CasoCavalloConfigurationFileHandler
from Utils.CasoCavalloConstants import REDIS_SERVER, CONFIGURATION_FILE_PATH, INITIAL_PERFORMANCES_TEST, \
    RANDOM_GENERATION_TIME, RANDOM_REMOVAL_TIME, RANDOM_THRESHOLD, USE_VIEWER
from Utils.PerformancesTests import initial_performances_test
from Utils.Workers.Generator import generator_worker
from Utils.Workers.Remover import remover_worker
from Utils.Workers.Viewer import viewer_worker


def random_remover(redis_client_to_use):

    while True:

        if redis_client_to_use.llen("random_bytes_32") > 0:
            redis_client_to_use.blpop("random_bytes_32", 1)

        if redis_client_to_use.llen("random_numbers_between_01") > 0:
            redis_client_to_use.blpop("random_numbers_between_01", 1)

        sleep(RANDOM_REMOVAL_TIME)


if __name__ == '__main__':
    """
    Main method
    """

    # ***** 1) Fetch random sources from configuration file *****
    random_sources = CasoCavalloConfigurationFileHandler\
        .load_random_sources_from_configuration_file(CONFIGURATION_FILE_PATH)

    # ***** 2) using existing random sources *****
    if random_sources:

        # Do initial performances test if required
        if INITIAL_PERFORMANCES_TEST:
            initial_performances_test(random_sources)

        # ***** 3) Start to generate randoms *****

        # Init redis server
        try:
            # Init redis server client
            redis_client = redis.Redis(
                host=REDIS_SERVER['host'],
                port=REDIS_SERVER['port'],
                db=REDIS_SERVER['database']
            )

            # 4) ***** Start a process for each random source *****

            # Load all queues from configuration file
            redis_queues = CasoCavalloConfigurationFileHandler\
                .load_queues_from_configuration_file(CONFIGURATION_FILE_PATH)

            # Get redis lists from queues
            redis_lists = [redis_queue['name'] for redis_queue in redis_queues]

            # Viewer process. It is for report functionalities
            if USE_VIEWER:
                viewer_process = Process(
                    target=viewer_worker,
                    args=(redis_client, redis_lists, )
                )
                viewer_process.start()

            # Delete all previous redis lists
            for redis_list in redis_lists:
                redis_client.delete(redis_list)

            # For each random source
            for random_source in random_sources:
                generator = Process(target=generator_worker, args=(redis_client, random_source, redis_queues, ))
                remover = Process(target=remover_worker, args=(redis_client, redis_lists, ))

                generator.start()
                remover.start()

        except Exception as exception:
            print(f"Error on init Redis\n{exception}")

    else:
        print("No random sources available!", file=sys.stderr)
