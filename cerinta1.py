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

dfa_echivalent = lnfa.transformareInDFA()

print("DFA echivalent:")
print(" ".join(dfa_echivalent.stari))
print(" ".join(dfa_echivalent.alfabet))
tranzitii_afisare_dfa = []
for s_plecare, cai in dfa_echivalent.legaturi.items():
    for lit, s_dest in cai.items():
        tranzitii_afisare_dfa.append(f"{s_plecare} {s_dest} {lit}")
print(len(tranzitii_afisare_dfa))
for t in tranzitii_afisare_dfa:
    print(t)
print(dfa_echivalent.stari[0])
print(" ".join(dfa_echivalent.stari_finale))

dfa_minim = dfa_echivalent.minimizare()

print("DFA minim:")
print(" ".join(dfa_minim.stari))
print(" ".join(dfa_minim.alfabet))
tranzitii_afisare_min = []
for s_plecare, cai in dfa_minim.legaturi.items():
    for lit, s_dest in cai.items():
        tranzitii_afisare_min.append(f"{s_plecare} {s_dest} {lit}")
print(len(tranzitii_afisare_min))
for t in tranzitii_afisare_min:
    print(t)
print(dfa_minim.stari[0])
print(" ".join(dfa_minim.stari_finale))
