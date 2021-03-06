# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 13:17:16 2018

@author: jarnd
"""

# Import the QISKit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import available_backends, execute
if __name__ == '__main__':
    # Create a Quantum Register with 2 qubits.
    q = QuantumRegister(3)
    # Create a Classical Register with 2 bits.
    c = ClassicalRegister(3)
    
    # Create a Quantum Circuit
    qc = QuantumCircuit(q, c)
    
    
    qc.h(q[0])
    
    
    # Swap gate between qubit 0 and 1 as 3 CX's
    # CX from qubit 1 to qubit 0
    qc.cx(q[1], q[0]) 
    # CX from qubit 0 to qubit 1 is not possible, flip using hadamards
    qc.h(q[0])
    qc.h(q[1])
    qc.cx(q[1], q[0])
    qc.h(q[0])
    qc.h(q[1])
    # CX from qubit 1 to qubit 0
    qc.cx(q[1], q[0])
    
    
    qc.measure(q, c)
    
    # See a list of available local simulators
    print("Local backends: ", available_backends({'local': True}))
    
    # Compile and run the Quantum circuit on a simulator backend
    job_sim = execute(qc, "local_qasm_simulator",shots=10000)
    sim_result = job_sim.result()
    
    # Show the results
    print("simulation: ", sim_result)
    print(sim_result.get_counts(qc))
 