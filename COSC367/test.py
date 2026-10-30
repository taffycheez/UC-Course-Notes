from itertools import product

def interpretations(atoms):
    atoms = sorted(atoms)
    return [dict(zip(atoms, values)) for values in product([False, True], repeat=len(atoms))]

atoms = {'q', 'p'}
for i in interpretations(atoms):
    print(i)