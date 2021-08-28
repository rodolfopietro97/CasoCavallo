from Utils.Tests.PerformancesTestsOnRandomBytes import performances_test_on_random_bytes


def performance_tester_worker(random_sources: dict):
    """
    Do all performance tests on random sources

    :param random_sources: Random sources to use

    """

    # Performances on random bytes
    for random_bytes_size in [32, 64, 128]:
        print(f"\n\n************************************************** Performance tests on random bytes of size "
              f"{random_bytes_size} **************************************************")
        performances_test_on_random_bytes(random_sources=random_sources,
                                          random_bytes_size=random_bytes_size)
