import os
os.environ["OMP_NUM_THREADS"] = "12"

import time
from qulacs import QuantumState
from qulacsplus.algorithms.benchmarking import QuantumVolume

def run_qv_circuits(n_qubits, n_trials):
    """
	Args:
		n_qubits <int>: number of qubits
		n_trials <int>: number of random circuits to create for each subset
	"""
    qv = QuantumVolume()
	# list of list of qubit subsets to generate QV circuits
	# assuming: n_qunits > 2
    qubit_lists = [list(range(n)) for n in range(3, n_qubits+1)]
	# QV sequences qv_circs, which is a list of lists of quantum volume circuits
    heavy_output_probs = [[] for _ in qubit_lists]
    qv_circs = qv.qv_circuits(qubit_lists=qubit_lists, ntrials=n_trials)
    for trial in range(n_trials):
        for idx, circuit in enumerate(qv_circs[trial]):
            state = QuantumState(circuit.get_qubit_count()) # |0>
            circuit.update_quantum_state(state)
            heavy_output_prob = qv.heavy_output_probability(state)
            # print(heavy_output_prob)
            heavy_output_probs[idx] += [heavy_output_prob]
    # validate(heavy_output_probs)

def validate(heavy_output_probs):
    """
	Checks if heavy-output probabilities are close to expected values.
	Heavy-output probability in ideal case must be around (1+ln2)/2 ~ 0.84567.

	Args:
		heavy_output_probs <list>: 
	"""
    for p_list in heavy_output_probs:
        average = sum(p_list) / len(p_list)
        # asymptotic ideal heavy output probability of (1+ln2)/2 ~ 0.847 (Aaronson, Chen)
        print('average:{}'.format(average))
	                 
if __name__ == "__main__":
	n_trials = 1024
	# min_measure_time = 1.0
	min_qubit = 3
	max_qubit = 4
	timeout = 60.

	for n in range(min_qubit, max_qubit+1):
		st = time.time()
		run_qv_circuits(n, n_trials)
		elp = time.time() - st
		print(n, elp)
		if(elp > timeout):
			break