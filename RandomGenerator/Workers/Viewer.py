from rich.console import Console
from rich.table import Table

from Utils.CasoCavalloConstants import VIEWER_MAXIMUM_ROWS


def viewer_worker(redis_client, redis_lists):
    """
    View in real time the redis queues.

    :param redis_client: Redis client ot use
    :param redis_lists: Redis lists names that we want show
    """

    # Create rich table
    table = Table(title=f"CasoCavallo real time randoms viewer", show_lines=True)

    # List of elements of each redis list. Each queue is a column
    elements_of_redis_lists = []

    # For each redis list
    for redis_list in redis_lists:
        # View size of redis list
        redis_list_size = redis_client.llen(redis_list)

        # Add header
        table.add_column(
            f"{redis_list} -> {redis_list_size} elements",
            justify="center",
            style="cyan"
        )

        # Get a string of elements of current lisy
        elements = "\n".join(
            [
                element.decode()
                for element in redis_client.lrange(redis_list,
                                                   0,
                                                   VIEWER_MAXIMUM_ROWS)
            ]
        )

        # Add current
        elements = elements + f"\n\nCURRENT: {redis_client.get(f'current_{redis_list}').decode()}"

        # Append elements of redis list (elements are expressed as string)
        elements_of_redis_lists.append(elements)

    # Add the tuple of list of redis lists expressed as string
    table.add_row(*tuple(elements_of_redis_lists))

    # Print final rich console
    console = Console()
    console.print(table)
