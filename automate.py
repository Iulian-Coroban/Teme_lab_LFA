class DFA:
    def __init__(self, alfabet, stari, stari_finale, legaturi):
        self.alfabet = set(alfabet)
        self.stari = stari
        self.stari_finale = stari_finale
        self.tranzitii_utilizate_la_ultima_verificare = []
        legaturidict = {}
        for legatura in legaturi:
            stare_initiala, stare_finala, litera = legatura.strip().split()
            if legaturidict.get(stare_initiala) is None:
                legaturidict[stare_initiala] = {litera : stare_finala}
            else:
                legaturidict[stare_initiala][litera] = stare_finala
        self.legaturi = legaturidict

    def verifica_cuvant(self, cuvant):
        self.tranzitii_utilizate_la_ultima_verificare = []
        stare_curenta = self.stari[0]
        for litera in cuvant:
            legaturi_stare_curenta = self.legaturi.get(stare_curenta, {})
            if legaturi_stare_curenta.get(litera) is None:
                return False
            self.tranzitii_utilizate_la_ultima_verificare.append((stare_curenta, litera))
            stare_curenta = legaturi_stare_curenta[litera]
        return stare_curenta in self.stari_finale

    def minimizare(self):
        stari_accesibile = set()
        coada = [self.stari[0]]
        while coada:
            stare = coada.pop(0)
            if stare not in stari_accesibile:
                stari_accesibile.add(stare)
                for litera in self.alfabet:
                    dest = self.legaturi.get(stare, {}).get(litera)
                    if dest:
                        coada.append(dest) 
        
        stari_filtrate = [s for s in self.stari if s in stari_accesibile]
        finale_filtrate = [s for s in self.stari_finale if s in stari_accesibile]
        non_finale = [s for s in stari_filtrate if s not in finale_filtrate]

        partitie = []
        if non_finale:
            partitie.append(tuple(non_finale))
        if finale_filtrate:
            partitie.append(tuple(finale_filtrate))

        while True:
            noua_partitie = []
            for grup in partitie:
                dictionar_semnaturi = {}
                for stare in grup:
                    semnatura = []
                    for litera in sorted(list(self.alfabet)):
                        dest = self.legaturi.get(stare, {}).get(litera)
                        clasa_dest = -1
                        for idx, g in enumerate(partitie):
                            if dest in g:
                                clasa_dest = idx
                                break
                        semnatura.append(clasa_dest)
                    semnatura = tuple(semnatura) 
                    if semnatura not in dictionar_semnaturi:
                        dictionar_semnaturi[semnatura] = [stare]
                    else:
                        dictionar_semnaturi[semnatura].append(stare)
                for s_grup in dictionar_semnaturi.values():
                    noua_partitie.append(tuple(s_grup)) 
            
            if len(noua_partitie) == len(partitie):
                break
            partitie = noua_partitie 

        stari_minime = []
        finale_minime = []
        legaturi_minime = []
        mapare_clasa = {}
        
        for i, grup in enumerate(partitie):
            nume_nou = f"M{i}"
            stari_minime.append(nume_nou)
            for s in grup:
                mapare_clasa[s] = nume_nou
                if s in finale_filtrate and nume_nou not in finale_minime:
                    finale_minime.append(nume_nou) 
        
        stare_start_veche = self.stari[0]
        nume_start_nou = mapare_clasa[stare_start_veche]
        stari_minime.remove(nume_start_nou)
        stari_minime.insert(0, nume_start_nou)
        for grup in partitie:
            reprezentant = grup[0]
            for litera in self.alfabet:
                dest_veche = self.legaturi.get(reprezentant, {}).get(litera)
                if dest_veche:
                    legaturi_minime.append(f"{mapare_clasa[reprezentant]} {mapare_clasa[dest_veche]} {litera}")
        
        return DFA(list(self.alfabet), stari_minime, finale_minime, legaturi_minime)

class NFA:
    def __init__(self, alfabet, stari, stari_finale, legaturi):
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

    def verifica_cuvant(self, cuvant):
        def recursie(stare_curenta, cuvant_curent):
            if len(cuvant_curent) == 0:
                return stare_curenta in self.stari_finale
            litera = cuvant_curent[0]
            legaturi_stare_curenta = self.legaturi.get(stare_curenta, {})
            stari_urmatoare = legaturi_stare_curenta.get(litera, [])
            for stare_urmatoare in stari_urmatoare:
                if recursie(stare_urmatoare, cuvant_curent[1:]):
                    return True
            return False
        return recursie(self.stari[0], cuvant)

class LAMBDA_NFA:
    def __init__(self, alfabet, stari, stari_finale, legaturi):
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

    def lambda_closure(self, stare):
        inchidere = {stare} 
        stiva = [stare]
        while stiva:
            stare_curenta = stiva.pop()
            leg = self.legaturi.get(stare_curenta, {}).get("lambda", [])
            for stare_urmatoare in leg:
                if stare_urmatoare not in inchidere:
                    inchidere.add(stare_urmatoare)
                    stiva.append(stare_urmatoare)
        return inchidere

    def transformareInDFA(self):
        start_closure = frozenset(self.lambda_closure(self.stari[0]))
        nume_stari = {start_closure: "S0"} 
        coada = [start_closure]
        tranzitiiDFA = []
        stariFinaleDfa = []
        while coada:
            stare_grup_curent = coada.pop(0)
            nume_s_curenta = nume_stari[stare_grup_curent]
            for s_nfa in stare_grup_curent:
                if s_nfa in self.stari_finale:
                    if nume_s_curenta not in stariFinaleDfa:
                        stariFinaleDfa.append(nume_s_curenta)
                    break 
            for litera in self.alfabet:
                if litera == "lambda": continue
                grup_urmator = set()
                for s_nfa in stare_grup_curent:
                    destinatii = self.legaturi.get(s_nfa, {}).get(litera, [])
                    for d in destinatii:
                        grup_urmator.update(self.lambda_closure(d))
                if grup_urmator:
                    f_grup_urmator = frozenset(grup_urmator)
                    if f_grup_urmator not in nume_stari:
                        nume_nou = f"S{len(nume_stari)}"
                        nume_stari[f_grup_urmator] = nume_nou
                        coada.append(f_grup_urmator)
                    nume_s_urmatoare = nume_stari[f_grup_urmator]
                    tranzitiiDFA.append(f"{nume_s_curenta} {nume_s_urmatoare} {litera}")
        return DFA(list(self.alfabet), list(nume_stari.values()), stariFinaleDfa, tranzitiiDFA)

    def conversieInAFE(self):
        tranzitii_afe = []
        for s_plecare, cai in self.legaturi.items():
            for simbol, stari_dest in cai.items():
                for s_dest in stari_dest:
                    tranzitii_afe.append(f"{s_plecare} {s_dest} {simbol}")
        return AFE(list(self.alfabet), self.stari, self.stari[0], self.stari_finale, tranzitii_afe)

    def transformareInExpresieRegulata(self):
        afe_obiect = self.conversieInAFE()
        return afe_obiect.transformare()

class AFE:
    def __init__(self, alfabet, stari, stare_start, stari_finale, tranzitii):
        self.alfabet = alfabet
        self.stari = stari[:]
        self.stare_start = stare_start
        self.stari_finale = stari_finale[:]
        legaturidict = {}
        for legatura in tranzitii:
            s_plecare, s_dest, simbol = legatura.strip().split()
            if simbol == "lambda": simbol = "λ"
            if s_plecare not in legaturidict: legaturidict[s_plecare] = {}
            if s_dest not in legaturidict[s_plecare]:
                legaturidict[s_plecare][s_dest] = simbol
            else:
                vechi = legaturidict[s_plecare][s_dest]
                legaturidict[s_plecare][s_dest] = f"({vechi}+{simbol})"
        self.legaturi = legaturidict

    def reuniune(self, r1, r2):
        if r1 == "0": return r2
        if r2 == "0": return r1
        if r1 == r2: return r1
        return f"({r1}+{r2})"

    def concatenare(self, r1, r2):
        if r1 == "0" or r2 == "0": return "0"
        if r1 == "λ": return r2
        if r2 == "λ": return r1
        return f"({r1}{r2})"

    def stelare(self, r):
        if r == "0" or r == "λ": return "λ"
        return f"({r}*)"

    def transformare(self):
        s_ini_noua = "START_AFE"
        s_fin_noua = "FINAL_AFE"
        self.stari.append(s_ini_noua)
        self.stari.append(s_fin_noua)
        if s_ini_noua not in self.legaturi: self.legaturi[s_ini_noua] = {}
        self.legaturi[s_ini_noua][self.stare_start] = "λ"
        for sf in self.stari_finale:
            if sf not in self.legaturi: self.legaturi[sf] = {}
            vechi = self.legaturi[sf].get(s_fin_noua, "0")
            self.legaturi[sf][s_fin_noua] = self.reuniune(vechi, "λ")
        stari_intermediare = [s for s in self.stari if s != s_ini_noua and s != s_fin_noua]
        for k in stari_intermediare:
            predecesori = [p for p in self.stari if p != k and self.legaturi.get(p, {}).get(k)]
            succesori = [s for s in self.stari if s != k and self.legaturi.get(k, {}).get(s)]
            r_kk = self.stelare(self.legaturi.get(k, {}).get(k, "0"))
            for p in predecesori:
                for s in succesori:
                    r_pk = self.legaturi[p][k]
                    r_kj = self.legaturi[k][s]
                    r_pj_vechi = self.legaturi[p].get(s, "0")
                    cale_noua = self.concatenare(self.concatenare(r_pk, r_kk), r_kj)
                    self.legaturi[p][s] = self.reuniune(r_pj_vechi, cale_noua)
            if k in self.legaturi: del self.legaturi[k]
            for p in self.stari:
                if k in self.legaturi.get(p, {}): del self.legaturi[p][k]
        return self.legaturi[s_ini_noua][s_fin_noua]
