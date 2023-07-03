from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.circuit.library import DraperQFTAdder

def addition(a, b):
    # Détermine le nombre de bits nécessaires pour représenter a et b
    n = max(len(bin(a)), len(bin(b))) - 2

    # Crée un registre quantique de taille 2n+1 pour les calculs
    q = QuantumRegister(2*n+1, 'q')
    # Crée un registre classique de taille n+1 pour stocker les résultats
    c = ClassicalRegister(n+1, 'c')

    # Crée un circuit quantique avec les registres q et c
    circuit = QuantumCircuit(q, c)

    # Convertit a et b en représentation binaire sur n bits, puis inverse l'ordre des bits
    a_binary = format(a, '0' + str(n) + 'b')[::-1]
    b_binary = format(b, '0' + str(n) + 'b')[::-1]

    # Applique les opérations de contrôle X aux qubits appropriés pour préparer les entrées
    for i in range(n):
        if a_binary[i] == '1':
            circuit.x(q[i])
        if b_binary[i] == '1':
            circuit.x(q[i+n])

    # Ajoute le circuit quantique de l'addition QFT de Draper
    circuit1 = DraperQFTAdder(num_state_qubits=n, kind="half")
    circuit = circuit.compose(circuit1)

    # Effectue des mesures sur les qubits appropriés pour obtenir les résultats classiques
    for i in range(n+1):
        circuit.measure(q[n+i], c[i])

    # Exécute le circuit sur un simulateur quantique
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=100)
    result = job.result()
    counts = result.get_counts()

    # Convertit le résultat binaire en décimal
    add_decimal = 0
    for count in counts:
        add_decimal = int(count[0::], 2)
    return add_decimal

for i in range(11):
    for j in range(11):
        assert addition(i,j) == i+j