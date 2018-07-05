# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:16:31 2018

@author: Jarnd
"""

# Import the QISKit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import register, available_backends, execute
import Qconfig

if __name__ == '__main__': 
    register(Qconfig.APItoken, Qconfig.config['url'])
    
    # Create a Quantum Register with 2 qubits.
    q = QuantumRegister(3)
    # Create a Classical Register with 2 bits.
    c = ClassicalRegister(3)
    # Create a Quantum Circuit
    qc = QuantumCircuit(q, c)
    
    # Hadamard on first qubit
    qc.h(q[0])
    
    # CX from 1 to 0
    qc.cx(q[1], q[0])
    
    # CX from 0 to 1 by hadamard flipping
    qc.h(q[0])
    qc.h(q[1])
    
    qc.cx(q[1], q[0])
    
    qc.h(q[0])
    qc.h(q[1])
    # CX from 1 to 0
    qc.cx(q[1], q[0])

    # Add a Measure gate to see the state.
    qc.measure(q, c)
    
    # See a list of available local simulators
    print("Local backends: ", available_backends({'local': True}))
    
    # Compile and run the Quantum circuit on a simulator backend
    job_sim = execute(qc, "local_unitary_simulator", shots=1000)
    sim_result = job_sim.result()
    
    # Show the results
    print("simulation: ", sim_result)
    print(sim_result.get_counts(qc))
