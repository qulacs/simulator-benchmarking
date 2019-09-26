import os
os.environ["OMP_NUM_THREADS"] = "12"

import time
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute
import qiskit.ignis.verification.quantum_volume as qv

def run_qv_circuits(n_qubits, n_trials, qr, qc, backend, basis_gates, shots):
	"""
	Args:
		n_qubits <int>: number of qubits
		n_trials <int>: number of random circuits to create for each subset
		qr <QuantumRegister>: instance of QuantumRegister
		qc <QuantumCircuit>: instance of QuantumCircuit
		backend <AerBackend>: instance of Aer backend
		basis_gates <list>: list of elementary gates
		shots <int>: number of sampling shots
	"""
	# list of list of qubit subsets to generate QV circuits
	# assuming: n_qunits > 2
	qubit_lists = [list(range(n)) for n in range(3, n_qubits+1)]
	# QV sequences qv_circs, which is a list of lists of quantum volume circuits
	qv_circs, qv_circs_nomeas = qv.qv_circuits(qubit_lists, n_trials, qr, qc)
	sampling_results = []
	for trial in range(n_trials):
		sampling_results += [execute(qv_circs[trial], basis_gates=basis_gates, backend=backend, shots=shots).result()]
	return sampling_results
	                 
if __name__ == "__main__":
	n_trials = 1024
	# min_measure_time = 1.0
	min_qubit = 3
	max_qubit = 4
	timeout = 60.

	backend = Aer.get_backend('qasm_simulator')
	basis_gates = ['u1', 'u2', 'u3', 'cx']
	shots = 1024
	for n in range(min_qubit, max_qubit+1):
		qr = QuantumRegister(n)
		qc = QuantumCircuit(qr)
		st = time.time()
		sampling_results = run_qv_circuits(n, n_trials, qr, qc, backend, basis_gates, shots)
		elp = time.time() - st
		print(n, elp)
		del qc
		del qr
		if(elp > timeout):
			break