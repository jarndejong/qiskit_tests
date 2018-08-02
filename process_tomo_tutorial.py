# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 17:28:02 2018

@author: Jarnd
"""

import sys, getpass
try:
    #sys.path.append("../../") # go to parent dir
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

# importing the QISKit
import qiskit
from qiskit import QuantumCircuit, QuantumProgram

# import tomography libary
import qiskit.tools.qcvv.tomography as tomo

# useful additional packages 
from qiskit.tools.visualization import plot_state
from qiskit.tools.qi.qi import *

# Creating registers
Q_program = QuantumProgram()

# Creating registers
qr = Q_program.create_quantum_register("qr", 2)
cr = Q_program.create_classical_register("cr", 2)

# hadamard on qubit-1 only
had = Q_program.create_circuit("had", [qr], [cr])
had.h(qr[1])

# CNOT gate with qubit 1 control, qubit 0 target (target for ibmqx4)
cnot = Q_program.create_circuit("cnot", [qr], [cr])
cnot.cx(qr[1], qr[0])

U_had = np.array([[1, 1], [1, -1]])/np.sqrt(2)
# compute Choi-matrix from unitary
had_choi = outer(vectorize(U_had))
plot_state(had_choi)

had_tomo_set = tomo.process_tomography_set([1],'Pauli','Pauli')
had_tomo_circuits = tomo.create_tomography_circuits(Q_program, 'had',qr,cr,had_tomo_set)


backend  =  'local_qasm_simulator'
shots = 1000
had_tomo_results = Q_program.execute(had_tomo_circuits, shots=shots, backend=backend)

had_process_data = tomo.tomography_data(had_tomo_results,'had', had_tomo_set)
had_choi_fit = tomo.fit_tomography_data(had_process_data,'leastsq',options={'trace':2})
plot_state(had_choi_fit,'paulivec')


#unitary matrix for CNOT with qubit 1 as control and qubit 0 as target.
U_cnot = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
# compute Choi-matrix from unitary
cnot_choi = outer(vectorize(U_cnot))
plot_state(cnot_choi)

cnot_tomo_set = tomo.process_tomography_set([1,0],'Pauli','Pauli')
cnot_tomo_circuits = tomo.create_tomography_circuits(Q_program,'cnot',qr,cr,cnot_tomo_set)

cnot_tomo_results = Q_program.execute(cnot_tomo_circuits, shots=shots, backend=backend,timeout=300)

cnot_process_data = tomo.tomography_data(cnot_tomo_results,'cnot',cnot_tomo_set)
cnot_choi_fit = tomo.fit_tomography_data(cnot_process_data,'leastsq',options={'trace':4})
plot_state(cnot_choi_fit,'city')

U_swap = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
swap_choi = outer(vectorize(U_swap))