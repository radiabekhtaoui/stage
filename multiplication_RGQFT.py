from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.circuit.library import RGQFTMultiplier

def multiplication(a, b):
    # Détermine le nombre de bits nécessaires pour représenter a et b
    n = max(len(bin(a)), len(bin(b))) - 2

    # Crée un registre quantique de taille 4n pour les calculs
    q = QuantumRegister(4*n, 'q')
    # Crée un registre classique de taille 2n pour stocker les résultats
    c = ClassicalRegister(2*n, 'c')

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

    # Ajoute le circuit quantique du multiplicateur QFT de RG
    circuit1 = RGQFTMultiplier(num_state_qubits=n, num_result_qubits=2*n)
    circuit = circuit.compose(circuit1)

    # Effectue des mesures sur les qubits appropriés pour obtenir les résultats classiques
    for i in range(2*n):
        circuit.measure(q[2*n+i], c[i])

    # Affiche le circuit quantique (commenté)
    #print(circuit)

    # Exécute le circuit sur un simulateur quantique
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=100)
    result = job.result()
    counts = result.get_counts()

    # Convertit le résultat binaire en décimal
    mul_decimal = 0
    for count in counts:
        mul_decimal = int(count[0::], 2)
    return mul_decimal

for i in range(11):
    for j in range(11):
        assert multiplication(i,j) == i*j