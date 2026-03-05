class DFA:
    alfabet = set()
    stari = []
    stari_finale = []
    legaturi = {}
    tranzitii_utilizate_la_ultima_verificare = []
    def __init__(self,alfabet, stari, stari_finale, legaturi):
        self.alfabet = set(alfabet)
        self.stari = stari
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
        stare_curenta = self.stari[0]
        for litera in cuvant:
            legaturi_stare_curenta = self.legaturi[stare_curenta]
            if legaturi_stare_curenta.get(litera) is None:
                return False
            self.tranzitii_utilizate_la_ultima_verificare.append((stare_curenta, litera))
            stare_curenta = legaturi_stare_curenta[litera]
        return stare_curenta in self.stari_finale

    def tranzitii_utilizate(self):
        return self.tranzitii_utilizate_la_ultima_verificare
    

class NFA:
    alfabet = set()
    stari = []
    stari_finale = []
    legaturi = {}
    tranzitii_utilizate_la_ultima_verificare = []
    def __init__(self,alfabet, stari, stari_finale, legaturi):
        self.alfabet = set(alfabet)
        self.stari = stari
        self.stari_finale = stari_finale
        legaturidict = {}
        for legatura in legaturi:
            stare_initiala, stare_finala, litera = legatura.strip().split()
            if legaturidict.get(stare_initiala) is None:
                legaturidict[stare_initiala] = {litera : [stare_finala]}
            else:
                if legaturidict[stare_initiala].get(litera) is None:
                    legaturidict[stare_initiala][litera] = [stare_finala]
                else:
                    legaturidict[stare_initiala][litera].append(stare_finala)
        self.legaturi = legaturidict

    def __str__(self):
        return ", ".join(self.alfabet)
    
    def verifica_cuvant(self, cuvant):
        def recursie(stare_curenta, cuvant_curent):
            if len(cuvant_curent) == 0:
                return stare_curenta in self.stari_finale
            litera = cuvant_curent[0]
            legaturi_stare_curenta = self.legaturi.get(stare_curenta, {})
            stari_urmatoare = legaturi_stare_curenta.get(litera, [])
            for stare_urmatoare in stari_urmatoare:
                self.tranzitii_utilizate_la_ultima_verificare.append((stare_curenta, litera))
                if recursie(stare_urmatoare, cuvant_curent[1:]):
                    return True
                self.tranzitii_utilizate_la_ultima_verificare.pop()
            return False
        return recursie(self.stari[0], cuvant)            

    def tranzitii_utilizate(self):
        return self.tranzitii_utilizate_la_ultima_verificare

    
#Verificari

d1 = DFA(("a", "b"), ["q0"], ["q1"], ["q0 q1 a", "q1 q0 b"])
print("DA" if d1.verifica_cuvant("a") else "Nu")
print(d1.tranzitii_utilizate())
print(d1)

n1 = NFA(("a", "b"), ["q0"], ["q1"], ["q0 q1 a", "q0 q1 b"])
print("Da" if n1.verifica_cuvant("a") else "Nu")
print(n1.tranzitii_utilizate())
print(n1)