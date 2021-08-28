from functools import reduce
import random

import numpy as np

from Utils.CasoCavalloConstants import HEX_ALPHABET, QUEUE_DATA_TYPES


class CasoCavalloOperations:
    """
    Operations class.

    It makes various operations on random numbers, such as XOR, etc...
    """

    @staticmethod
    def bytes_xor(bytes1: str, bytes2: str):
        """
        Make xor between two bytes expressed as string

        :param bytes1: Random bytes 1
        :param bytes2: Random bytes 2
        :return: Xor by bytes1 and bytes2
        """

        # Bytes must have same size
        assert len(bytes1) == len(bytes2)

        # Get indices (in our case number) of every alphabet symbols.
        # Every index correspond to a character: Index 0->'0', ... , Index 15->'f'
        # With one to one correspondence we make xor on indexes
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

        # Return for each index the corresponding character. ALl as a string
        return ''.join(
            [
                HEX_ALPHABET[index]
                for index in np.nditer(indices_xor)
            ]
        )

    @staticmethod
    def reduce_randoms(randoms_list: list, datatype: str):
        """
        Find correct reduction for datatype.

        The main concept of CasoCavallo is to obtain truly random numbers
        by using Pseudo Random numbers "merged" to truly random numbers
        or to other pseudo random numbers.

        To do this merge we need specific "merge" operations.

        For example:
        * Random bytes can be merged with xor
        * Etc..

        :param randoms_list: Random list to reduce
        :param datatype: Datatype of random list

        :return: Random number obtained by reduction on random_list
        """

        # # Random list must not be empty
        # assert len(randoms_list) > 0
        #
        # # Random list must have a valid datatype
        # assert datatype not in QUEUE_DATA_TYPES

        # Default we don't have a result
        reduction_result = None

        # Reduction function for random bytes
        if datatype == "RANDOM_BYTES":
            # Reduce with xor
            reduction_result = reduce(CasoCavalloOperations.bytes_xor, randoms_list)

        # Reduction function for binaries
        if datatype == "BINARY":
            # Convert to float
            randoms_list = map(float, randoms_list)
            reduction_result = reduce(lambda r1, r2: r1 if random.uniform(0, 1) >= 0.5 else r2, randoms_list)

        # Reduction function for integers
        if datatype == "INTEGER":
            # Convert to int
            randoms_list = map(int, randoms_list)
            reduction_result = reduce(lambda r1, r2: r1 if random.uniform(0, 1) >= 0.5 else r2, randoms_list)

        # Reduction function for reals
        if datatype == "REAL":
            # Convert to float
            randoms_list = map(float, randoms_list)
            reduction_result = reduce(lambda r1, r2: r1 + r2, randoms_list)

        return reduction_result
