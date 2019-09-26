import os
os.environ["OMP_NUM_THREADS"] = "12"

import time
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute
import qiskit.ignis.verification.quantum_volume as qv

def run_qv_circuits(n_qubits, n_trials, qr, qc, backend):
	"""
	Args:
		n_qubits <int>: number of qubits
		n_trials <int>: number of random circuits to create for each subset
		qr <QuantumRegister>: instance of QuantumRegister
		qc <QuantumCircuit>: instance of QuantumCircuit
		backend <AerBackend>: instance of Aer backend
	"""
	# list of list of qubit subsets to generate QV circuits
	# assuming: n_qunits > 2
	qubit_lists = [list(range(n)) for n in range(3, n_qubits+1)]
	# QV sequences qv_circs, which is a list of lists of quantum volume circuits
	_, qv_circs_nomeas = qv.qv_circuits(qubit_lists, n_trials, qr, qc)
	ideal_results = []
	for trial in range(n_trials):
		ideal_results += [execute(qv_circs_nomeas[trial], backend=backend).result()]
	# validate(qubit_lists, ideal_results)
	return ideal_results

def validate(qubit_lists, ideal_results):
	"""
	Checks if heavy-output probabilities are close to expected values.
	Heavy-output probability in ideal case must be around (1+ln2)/2 ~ 0.84567.

	Args:
		qubit_lists <list>: list of list of qubit subsets to generate QV circuits
		ideal_results <dict>: job results
	"""
	qv_fitter = qv.QVFitter(qubit_lists=qubit_lists)
	qv_fitter.add_statevectors(ideal_results)
	for qubit_list in qubit_lists:
		l = len(qubit_list)
		key = 'qv_depth_' + str(l) + '_trial_0'
		prob = qv_fitter._heavy_output_prob_ideal[key]
		print(prob)
	                 
if __name__ == "__main__":
	n_trials = 1024
	# min_measure_time = 1.0
	min_qubit = 3
	max_qubit = 4
	timeout = 60.

	backend = Aer.get_backend('statevector_simulator')
	for n in range(min_qubit, max_qubit+1):
		qr = QuantumRegister(n)
		qc = QuantumCircuit(qr)
		st = time.time()
		ideal_results = run_qv_circuits(n, n_trials, qr, qc, backend)
		elp = time.time() - st
		print(n, elp)
		del qc
		del qr
		if(elp > timeout):
			break