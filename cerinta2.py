from automate import LAMBDA_NFA

nume_fisier = input()
f = open(nume_fisier)

stari = f.readline().strip().split()
alfabet = f.readline().strip().split()
nr_tranzitii = int(f.readline().strip())
tranzitii = [f.readline().strip() for _ in range(nr_tranzitii)]
stare_initiala = f.readline().strip()
stari_finale = f.readline().strip().split()

if stare_initiala in stari:
    stari.remove(stare_initiala)
stari.insert(0, stare_initiala)

lnfa = LAMBDA_NFA(alfabet, stari, stari_finale, tranzitii)

expresie_regulata = lnfa.transformareInExpresieRegulata()

print("Expresie Regulata:")
print(expresie_regulata)
