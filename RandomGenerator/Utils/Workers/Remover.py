from time import sleep

from Utils.CasoCavalloConstants import RANDOM_REMOVAL_TIME


def remover_worker(redis_client, redis_lists):
    while True:

        for redis_list in redis_lists:
            if redis_client.llen(redis_list) > 0:
                redis_client.blpop(redis_list, 1)

        sleep(RANDOM_REMOVAL_TIME)
