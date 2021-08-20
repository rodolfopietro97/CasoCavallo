from functools import reduce
from math import floor
import random
from statistics import mean

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

    @staticmethod
    def reduce_randoms(randoms_list, datatype):
        """
        Find correct reduction for datatype.

        :param randoms_list: Random list to reduce
        :param datatype: Datatype of random list

        :return: Random number chooses with reduction
        """

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
