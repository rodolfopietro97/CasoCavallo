import os


def server_worker(redis_client, redis_lists, cummare_clients_path, picinusu_fetcher_path, cummare_server):
    """
    Real time server.
    Every seconds it handle random requests and push random responses

    :param redis_client: Redis client ot use
    :param redis_lists: Redis lists names that we want show
    :param cummare_clients_path: Path of cummare js clients
    :param picinusu_fetcher_path: Path of Picinusu clients
    :param cummare_server: Address of CUmmare Server
    """

    # For each redis list
    picinusu_fetcher_queues_args = "".join([f" {queue} {redis_client.get(f'current_{queue}').decode()}" for queue in redis_lists])

    # Final command
    command = f"python {picinusu_fetcher_path} {cummare_clients_path} {cummare_server} {picinusu_fetcher_queues_args}"
    os.system(command)
