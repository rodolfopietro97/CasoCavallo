from RandomSources.CasoCavalloRandomSource import CasoCavalloRandomSource
import random


class SimpleExternalRandomSource(CasoCavalloRandomSource):
    """
    Implementation of simple extenral random source

    To implement your custom random source, you must:
        - 1) Define get_normal_random function by using your device specification
        - 2) Add the import of this class in Externals.copy()
        - 3) Define this class in Configuration file
    """

    def get_normal_random(self):
        """
        Definition of get normal random function.

        It return a number between 0 and 1

        :return: A random number between 0 and 1 using external device
        """

        # QUISKIT EXAMPLE - https://towardsdatascience.com/flip-a-coin-on-a-real-quantum-computer-in-python-df51e5f2367b
        # Create circuit with 1 quantum and 1 classical bit
        # circuit = QuantumCircuit(1, 1)

        # Apply Hadamard gate to quantum bit --> Superposition
        # circuit.h(0)

        # Execute over a real quantumn computer
        # provider = IBMQ.enable_account("...")
        # quantum_computer = provider.get_backend("...")
        # job = execute(circuit, quantum_computer, shots=1)

        # result = job.result()
        # print(result.get_statevector())

        return random.uniform(0, 1)
