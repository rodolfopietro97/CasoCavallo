from time import sleep

from Utils.CasoCavalloConstants import RANDOM_REMOVAL_TIME


def remover_worker(redis_client, redis_lists):
    """
    Remove elements from redis queues

    :param redis_client: Redis client to use
    :param redis_lists: Redis queues names
    """

    while True:

        for redis_list in redis_lists:
            if redis_client.llen(redis_list) > 0:
                redis_client.blpop(redis_list, 1)

        sleep(RANDOM_REMOVAL_TIME)
