from RandomSources.CasoCavalloRandomSource import CasoCavalloRandomSource
import random
from qiskit import *


class QiskitRandomSource(CasoCavalloRandomSource):
    """
    Implementation of Qiskit random source.

    It uses quantum circuit in order to generate a number between 0 and 1
    """

    def get_normal_random(self):
        """
        Definition of get normal random function.

        It return a number between 0 and 1

        :return: A random number between 0 and 1 using python libraries
        """

        # Create circuit with 1 quantum and 1 classical bit
        circuit = QuantumCircuit(1, 1)

        # Apply Hadamard gate to quantum bit --> Superposition
        circuit.h(0)



        # Execute quantum circuit once ("shots") on real quantum computer "ibmq_armonk"
        provider = IBMQ.enable_account("324a3107a62f2e90dd76760b003f4a087f347b38d255ea5d3a1bf843b3e4ccc69de783dc98edb31fc6b35935ebdb996c83b42ddbbe80c6a477eaf876d7e0a7a5")
        quantum_computer = provider.get_backend("ibmq_armonk")
        job = execute(circuit, quantum_computer, shots=1)

        # Extract result and print it
        result = job.result()
        print(result.get_statevector())

        return random.uniform(0, 1)
