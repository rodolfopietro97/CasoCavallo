from time import sleep

from Utils.CasoCavalloConstants import RANDOM_GENERATION_TIME, RANDOM_THRESHOLD


def generator_worker(redis_client, random_source, redis_queues):
    """
    For a specific random source this function start a main loop of insertion of random number

    :param redis_client: Redis client ot use
    :param random_source: Random source to use
    :param redis_queues: Redis queues to fill
    """

    # Run forever
    while True:

        # For each redis queue
        for redis_queue in redis_queues:
            # If queue is not empty
            if redis_client.llen(redis_queue['name']) < RANDOM_THRESHOLD:

                # Default equal 0
                current_random = 0

                # BINARY data type
                if redis_queue['type'] == "BINARY":
                    current_random = random_source().get_normal_random()

                # BYTES Data type
                if redis_queue['type'] == "RANDOM_BYTES":
                    current_random = random_source().get_random_bytes(size=redis_queue['size'])

                # INTEGER Data types
                if redis_queue['type'] == "INTEGER":
                    current_random = random_source().get_random_range_int(minimum=redis_queue['range'][0],
                                                                          maximum=redis_queue['range'][1])

                # REAL Data types
                if redis_queue['type'] == "REAL":
                    current_random = random_source().get_random_range(minimum=redis_queue['range'][0],
                                                                          maximum=redis_queue['range'][1])

                # Final push on queue
                redis_client.rpush(redis_queue['name'], f"{current_random}")

        sleep(RANDOM_GENERATION_TIME)
