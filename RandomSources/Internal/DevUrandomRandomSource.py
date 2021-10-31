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

        :return: A random number between 0 and 1 using /dev/urandom linux file
        """

        # Default random number is 0 if any errors
        random_number = 0

        # Open /dev/urandom file
        with open("/dev/urandom", 'rb') as file:
            # Divide the number for 255 to obtain a normalized number in the interval [0;1]
            random_number = int.from_bytes(file.read(1), "little") / 255

        return random_number
