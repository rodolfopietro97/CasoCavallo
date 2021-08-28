import abc

from Utils.CasoCavalloConstants import HEX_ALPHABET


class CasoCavalloRandomSource(abc.ABC):
    """
    This class represent the abstraction of a Random Source.

    Random source is a source capable to generate random numbers.

    It can be of two kinds:
        * Internal: If uses an internal technology, such as /dev/urandom or classical random sequences
        * External: If uses external random sources, such as Quantum computer, Hardware devices, and other stuff...

    The Children of this class must only to redefine **get_normal_random()** function.
    All other functions derives from this function.
    """

    def __init__(self):
        """
        Default constructor
        """

        pass

    @abc.abstractmethod
    def get_normal_random(self):
        """
        Main abstract method.

        It return random between 0 and 1

        :return: A random between 0 and 1
        """

        pass

    def get_random_bytes(self, size: int):
        """
        Return a random byte of size bytes.

        :return: A random bytes
        """

        # Random bytes must have a size.
        assert size > 0

        # List of bytes.
        bytes_list = [
            # Every hex digit is a random between 0 and 15
            HEX_ALPHABET[
                self.get_random_range_int(minimum=0, maximum=15)
            ]
            for _ in range(size)
        ]

        # Return the random bytes as a string
        return ''.join(bytes_list)

    def get_random_range(self, minimum: float, maximum: float):
        """
        Generate a random number between minimum and maximum

        :param minimum: Lower bound
        :param maximum: Upper bound

        :return: A random number between minimum and maximum
        """

        # Minimum must not be great equal than maximum
        assert minimum < maximum

        # Denormalize a random using [minimum; maximum] range, start from [0;1] range
        return minimum + (self.get_normal_random() * (maximum - minimum))

    def get_random_range_int(self, minimum: int, maximum: int):
        """
        Generate a integer random number between minimum and maximum

        :param minimum: Lower bound
        :param maximum: Upper bound

        :return: A integer random number between minimum and maximum
        """

        # Minimum must not be great equal than maximum
        assert minimum < maximum

        # Return the integer of get_random_range_int
        return int(self.get_random_range(minimum=minimum, maximum=maximum))
