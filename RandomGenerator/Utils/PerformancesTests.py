import time

from Utils.CasoCavalloOperations import CasoCavalloOperations


def initial_performances_test(random_sources):
    """
    Do initial performances test

    How many pairs of random bytes of size 32 we can generate in 1 second.

    More after every generation we do xor

    :param random_sources: List of random sources to test
    :return:
    """

    # For each random source
    for random_source in random_sources:
        start = time.time()
        end = start
        count = 0

        # Work for 1 second
        while end - start < 1:

            # Generate random bytes
            random_bytes1 = random_source().get_random_bytes(size=32)
            random_bytes2 = random_source().get_random_bytes(size=32)

            # Do xor
            xor = CasoCavalloOperations.bytes_xor(random_bytes1, random_bytes2)

            count = count + 1
            end = time.time()

        # Final report
        print(f"In {end-start} second, generated {count} 32 bytes size random bytes."
              f" (with doing everytime xor)."
              f" Using {random_source}")