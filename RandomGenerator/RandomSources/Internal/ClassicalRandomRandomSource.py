from RandomSources.CasoCavalloRandomSource import CasoCavalloRandomSource
import random


class ClassicalRandomRandomSource(CasoCavalloRandomSource):
    """
    Implementation of Local random source.

    It uses random functions of python library
    """

    def get_normal_random(self):
        """
        Definition of get normal random function.

        It return a number between 0 and 1

        :return: A random number between 0 and 1 using python libraries
        """

        return random.uniform(0, 1)
