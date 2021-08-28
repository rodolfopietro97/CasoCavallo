from time import sleep

import numpy as np

from Utils.CasoCavalloConstants import \
    MERGER_BUFFER_SIZE, \
    MERGER_MERGE_TIME
from Utils.CasoCavalloOperations import CasoCavalloOperations


def merger_worker(redis_client, redis_queues):
    # Run forever
    while True:

        # For each redis queue
        for redis_queue in redis_queues:

            # All operations can start if and only if redis queue has elements!
            if redis_client.llen(redis_queue['name']) > 0:

                # If we have at least MERGER_BUFFER_SIZE elements we take all array
                if redis_client.llen(redis_queue['name']) <= MERGER_BUFFER_SIZE:
                    random_chooses_randoms = np.array(
                        [element.decode()
                         for element in redis_client.lrange(
                            redis_queue['name'],
                            0,
                            -1)
                         ]
                    )
                # More than MERGER_BUFFER_SIZE elements. We need a random sample
                else:
                    # List of random chooses form the queue on which we apply our operation
                    random_chooses_randoms = np.array(
                        [element.decode()
                         for element in redis_client.lrange(
                            redis_queue['name'],
                            0,
                            -1)
                         ]
                    )
                    # Choose without replacement
                    random_chooses_randoms = np.random.choice(
                        random_chooses_randoms,
                        size=MERGER_BUFFER_SIZE,
                        replace=False
                    )

                # Set current random dependently by datatype and strategy to use for particular datatype
                current_random = CasoCavalloOperations.reduce_randoms(
                    randoms_list=random_chooses_randoms.tolist(),
                    datatype=redis_queue['type']
                )

                # Push random in redis
                redis_client.set(f"current_{redis_queue['name']}", current_random)

        sleep(MERGER_MERGE_TIME)
