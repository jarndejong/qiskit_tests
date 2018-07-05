// Name of Experiment: FT SWAP gate with 3 swap gates including 1 ancilla v3

OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

x q[0];
h q[1];
h q[2];
barrier q[0],q[1],q[2],q[3],q[4];
cx q[2],q[0];
h q[0];
h q[2];
cx q[2],q[0];
h q[0];
h q[2];
cx q[2],q[0];
barrier q[0],q[1],q[2],q[3],q[4];
cx q[1],q[0];
h q[0];
h q[1];
cx q[1],q[0];
h q[0];
h q[1];
cx q[1],q[0];
barrier q[0],q[1],q[2],q[3],q[4];
cx q[2],q[1];
h q[1];
h q[2];
cx q[2],q[1];
h q[1];
h q[2];
cx q[2],q[1];
barrier q[0],q[1],q[2],q[3],q[4];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
