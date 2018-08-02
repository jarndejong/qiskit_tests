# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 16:14:11 2018

@author: Jarnd
"""

import sys, getpass
try:
    import Qconfig
    qx_config = {
        "APItoken": Qconfig.APItoken,
        "url": Qconfig.config['url']}
    print('Qconfig loaded from %s.' % Qconfig.__file__)
except:
    APItoken = getpass.getpass('Please input your token and hit enter: ')
    qx_config = {
        "APItoken": APItoken,
        "url":"https://quantumexperience.ng.bluemix.net/api"}
    print('Qconfig.py not found in qiskit-tutorial directory; Qconfig loaded using user input.')
    
import numpy as np
from time import sleep  # used for polling jobs
    
# importing the QISKit
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, QuantumProgram

# import tomography library
import qiskit.tools.qcvv.tomography as tomo

# useful additional packages 
from qiskit.tools.visualization import plot_state, plot_histogram
from qiskit.tools.qi.qi import state_fidelity, concurrence, purity, outer


# Create a 2-qubit quantum register# Creat
qr = QuantumRegister(2)
cr = ClassicalRegister(2)

# quantum circuit to make an entangled Bell state
bell = QuantumCircuit(qr, cr, name='bell')
bell.h(qr[1])
bell.cx(qr[1], qr[0])

#print(qiskit.available_backends())
job = qiskit.execute(bell, backend='local_statevector_simulator')
bell_psi = job.result().get_statevector(bell)
bell_rho = outer(bell_psi) # construct the density matrix from the state vector

#plot the state
plot_state(bell_rho,'paulivec')


# Construct state tomography set for measurement of qubits [0, 1] in the Pauli basis
bell_tomo_set = tomo.state_tomography_set([0, 1])

# Create a quantum program containing the state preparation circuit
Q_program = QuantumProgram()
Q_program.add_circuit('bell', bell)

# Add the state tomography measurement circuits to the Quantum Program
bell_tomo_circuit_names = tomo.create_tomography_circuits(Q_program, 'bell', qr, cr, bell_tomo_set)

print('Created State tomography circuits:')
for name in bell_tomo_circuit_names:
    print(name)
    

# Use the local simulator# Use t 
backend = 'local_qasm_simulator'

# Take 5000 shots for each measurement basis
shots = 5000

# Run the simulation
bell_tomo_result = Q_program.execute(bell_tomo_circuit_names, backend=backend, shots=shots)
print(bell_tomo_result)

bell_tomo_data = tomo.tomography_data(bell_tomo_result, 'bell', bell_tomo_set)

rho_fit = tomo.fit_tomography_data(bell_tomo_data)

# calculate fidelity, concurrence and purity of fitted state# calcul 
F_fit = state_fidelity(rho_fit, bell_psi)
con = concurrence(rho_fit)
pur = purity(rho_fit)

# plot 
plot_state(rho_fit, 'paulivec')
plot_state(rho_fit,'city')
print('Fidelity =', F_fit)
print('concurrence = ', str(con))
print('purity = ', str(pur))