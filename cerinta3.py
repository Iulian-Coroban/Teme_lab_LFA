from automate import Gramatica

nume_fisier = input()
f = open(nume_fisier)

neterminale = f.readline().strip().split()
terminale = f.readline().strip().split()
nr_productii = int(f.readline().strip())
productii = [f.readline().strip() for _ in range(nr_productii)]
simbol_start = f.readline().strip()
lungime_x = int(f.readline().strip())

g = Gramatica(neterminale, terminale, productii, simbol_start)
rezultate = g.genereaza_cuvinte(lungime_x)

if not rezultate:
    print("NU EXISTA")
else:
    for cuvant in rezultate:
        print(cuvant)
