# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 14:29:46 2018

@author: jarnd
"""

# Import the QISKit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QuantumProgram
from qiskit import available_backends, execute
from qiskit.tools.visualization import circuit_drawer
import qiskit.tools.qcvv.tomography as tomo

if __name__ == '__main__':
    # Create a Quantum Register with 2 qubits.
    q = QuantumRegister(3)
    # Create a Classical Register with 2 bits.
    c = ClassicalRegister(3)
    
    # Create a Quantum Circuit
    qc = QuantumCircuit(q, c)
    
    
    # Swap gate between qubit 0 and 2 as 3 CX's
    # CX from qubit 2 to qubit 0
    qc.cx(q[2], q[0]) 
    # CX from qubit 0 to qubit 2 is not possible, flip using hadamards
    qc.h(q[0])
    qc.h(q[2])
    qc.cx(q[2], q[0])
    qc.h(q[0])
    qc.h(q[2])
    # CX from qubit 1 to qubit 0
    qc.cx(q[2], q[0])
    
    
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
    
    # Swap gate between qubit 1 and 2 as 3 CX's
    # CX from qubit 2 to qubit 1
    qc.cx(q[2], q[1]) 
    # CX from qubit 1 to qubit 2 is not possible, flip using hadamards
    qc.h(q[1])
    qc.h(q[2])
    qc.cx(q[2], q[1])
    qc.h(q[1])
    qc.h(q[2])
    # CX from qubit 1 to qubit 0
    qc.cx(q[2], q[1])
    
    
    
    # Post circuit operations
    qc.measure(q, c)
    
    # See a list of available local simulators
    print("Local backends: ", available_backends({'local': True}))
    
    # Compile and run the Quantum circuit on a simulator backend
    job_sim = execute(qc, "local_qasm_simulator",shots=10)
    sim_result = job_sim.result()
    
    # Create a quantum program for the process tomography simulation
    processprogram = QuantumProgram()
    processprogram.add_circuit('FTSWAP', qc)
    
    # Create registers for the process tomography
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    
    # Create the tomography set
    tomo_set = tomo.process_tomography_set([1, 0],'Pauli','Pauli')
    tomo_circuits = tomo.create_tomography_circuits(processprogram, 'FTSWAP',qr,cr,tomo_set)
    
    
    # Use the local simulator# Use t 
    backend = 'local_qasm_simulator'

    # Take 5000 shots for each measurement basis
    shots = 500

    # Run the simulation
    tomo_result = processprogram.execute(tomo_circuits, backend=backend, shots=shots)
    
    tomo_data = tomo.tomography_data(tomo_result, 'FTSWAP', tomo_set)

    #rho_fit = tomo.fit_tomography_data(tomo_data)
    
    #plot_state(rho_fit, 'paulivec')
