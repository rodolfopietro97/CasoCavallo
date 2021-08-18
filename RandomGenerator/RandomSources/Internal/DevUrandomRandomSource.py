from RandomSources.CasoCavalloRandomSource import CasoCavalloRandomSource


class DevUrandomRandomSource(CasoCavalloRandomSource):
    """
    Implementation of Local random source.

    It uses /dev/urandom.
    """

    def get_normal_random(self):
        """
        Definition of get normal random function.

        It return a number between 0 and 1
        :return:
        """

        # Default random number is 0 if any errors
        random_number = 0

        # Use /dev/urandom file
        with open("/dev/urandom", 'rb') as file:
            random_number = int.from_bytes(file.read(1), "little") / 255

        return random_number
