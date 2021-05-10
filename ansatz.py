from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import itertools
import numpy as np

def possible_pair(type,interaction,n_spins):

    # give all possible list of ascending integers between  i and j

    List=[]
    if type == 'linear':
        for j in range(1,interaction+1):
            for i in range(n_spins-1):
                if i+j>n_spins-1:
                    continue
                a=[i]
                for k in range(j):
                    a.append(i+k+1)
                List.append(a)

    elif type == 'circular':

        for j in range(1,interaction+1):
            for i in range(n_spins):
                if i+j>n_spins:
                    continue
                a=[i]
                for k in range(j):
                    a.append((i+k+1)%n_spins)
                List.append(a)

    elif type == 'full':
        for i in range(n_spins):
            for j in range(i+1,n_spins):
                for l in range(j-i):
                    a=[i]
                    b = itertools.combinations(range(i+1,j),l)
                    for it in b:
                        c = a+list(it)
                        c.append(j)
                        List.append(c)
    else:
        print('entanglement type not valid')
    c=0
    for a in range(len(List)):
        if len(List[a-c])>interaction+1 :
            del List[a-c]
            c+=1

    return List


def feature_map_ansatz(parameter,n_spins,n_layer,entanglement_type='full', interaction_length=2, full_rotation='False'):
    '''ansatz composed of y rotation followed by a trainable feature map
    len(parameter)=[(1+2*full_rotation)*n_spins+len(int_list)]*n_layer
    '''
	int_list=possible_pair(entanglement_type,interaction_length,n_spins)
	count = 0
	circuit = QuantumCircuit(n_spins)

    for i in range(n_layer):
        #y-rotation
        for j in range(n_spins):
            circuit.ry(parameter[count],j)
            count = count +1
            if full_rotation:
                circuit.rx(parameter[count],j)
                count = count +1
                circuit.ry(parameter[count],j)
                count = count +1

        #trainable feature map
        for interaction in int_list:
            for j in range(len(interaction_length)-1):
                circuit.cx(interaction[j],interaction[j+1]%n_spins)
                circuit.rz(parameter[count],interaction[-1]%n_spins)
                count += 1
            for j in reversed(range(len(interaction)-1)):
                circuit.cx(interaction[j],interaction[j+1]%n_spins)
    return circuit
