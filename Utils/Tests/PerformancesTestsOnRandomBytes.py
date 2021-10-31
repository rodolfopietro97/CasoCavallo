import time

from Utils.CasoCavalloOperations import CasoCavalloOperations


def performances_test_on_random_bytes(random_sources: dict, random_bytes_size: int):
    """
    Do initial performances test on random bytes.

    How many pairs of random bytes of size **random_bytes_size** we can generate in 1 second.

    More after every generation we do xor

    :param random_sources: List of random sources to test
    :param random_bytes_size: Size of random bytes to tests

    """

    # For each random source
    for random_source in random_sources:
        start = time.time()
        end = start
        count = 0

        # Work for 1 second
        while end - start < 1:

            # Generate random bytes
            random_bytes1 = random_source().get_random_bytes(size=random_bytes_size)
            random_bytes2 = random_source().get_random_bytes(size=random_bytes_size)

            # Do xor
            CasoCavalloOperations.bytes_xor(random_bytes1, random_bytes2)

            count = count + 1
            end = time.time()

        # Final report
        print(
            f"\n\t*\t{count} Random Bytes in {end-start} seconds. (with doing everytime xor)."
            f"\n\t\t\tRandom source: {random_source}"
        )
