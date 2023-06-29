
from qiskit.circuit.library import DraperQFTAdder,RGQFTMultiplier

def multiplication(a, b,circuit, n):
    
    circuit1 = RGQFTMultiplier(num_state_qubits=n, num_result_qubits=2*n)
    circuit = circuit.compose(circuit1)
    return circuit

def addition(a, b,circuit, n):
    
    circuit1 = DraperQFTAdder(num_state_qubits=n,kind="half")
    circuit = circuit.compose(circuit1)
    return circuit