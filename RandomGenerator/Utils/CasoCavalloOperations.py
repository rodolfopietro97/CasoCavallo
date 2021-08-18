import numpy as np

from Utils.CasoCavalloConstants import HEX_ALPHABET


class CasoCavalloOperations:
    """
    Operations class.

    It makes various operations on random numbers, such as XOR, ...
    """

    @staticmethod
    def bytes_xor(bytes1, bytes2):
        """
        Make xor between two bytes expressed as string

        :param bytes1: Random bytes 1
        :param bytes2: Random bytes 2
        :return: Xor by bytes1 and bytes2
        """

        # Bytes must have same size
        assert len(bytes1) == len(bytes2)

        # Get indices (in our case number) of every alphabet symbols
        # -example- '0'=0, ..., 'f'=15
        indices_bytes1 = np.array(
            [HEX_ALPHABET.index(element)
             for element in bytes1]
        )

        indices_bytes2 = np.array(
            [HEX_ALPHABET.index(element)
             for element in bytes2]
        )

        # Make xor of numbers
        indices_xor = indices_bytes1 ^ indices_bytes2

        # Return the string of all indexes
        return ''.join(
            [HEX_ALPHABET[index]
             for index in np.nditer(indices_xor)]
        )
