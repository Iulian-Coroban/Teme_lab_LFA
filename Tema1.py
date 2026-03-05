class DFA:
    alfabet = set()
    stari_initiale = []
    stari_finale = []
    legaturi = {}
    tranzitii_utilizate_la_ultima_verificare = []
    def __init__(self,alfabet, stari_initiale, stari_finale, legaturi):
        self.alfabet = set(alfabet)
        self.stari_initiale = stari_initiale
        self.stari_finale = stari_finale
        legaturidict = {}
        for legatura in legaturi:
            stare_initiala, stare_finala, litera = legatura.strip().split()
            if legaturidict.get(stare_initiala) is None:
                legaturidict[stare_initiala] = {litera : stare_finala}
            else:
                if legaturidict[stare_initiala].get(litera) is None:
                    legaturidict[stare_initiala][litera] = stare_finala
                else:
                    print("Acesta print definitie ar trebui sa fie un DFA, dar exista o legatura dubla pentru starea " + stare_initiala + " si litera " + litera)
                    return False
        self.legaturi = legaturidict

    def __str__(self):
        return ", ".join(self.alfabet)
    
    def verifica_cuvant(self, cuvant):
        stare_curenta = self.stari_initiale[0]
        for litera in cuvant:
            legaturi_stare_curenta = self.legaturi[stare_curenta]
            if legaturi_stare_curenta.get(litera) is None:
                return False
            self.tranzitii_utilizate_la_ultima_verificare.append((stare_curenta, litera))
            stare_curenta = legaturi_stare_curenta[litera]
        return stare_curenta in self.stari_finale

    def tranzitii_utilizate(self):
        return self.tranzitii_utilizate_la_ultima_verificare

    
#Verificari

d1 = DFA(("a", "b"), ["q0"], ["q1"], ["q0 q1 a", "q1 q0 b"])
print(d1.verifica_cuvant("a"))
print(d1.tranzitii_utilizate())
print(d1)