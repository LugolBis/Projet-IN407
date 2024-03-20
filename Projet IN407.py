### Projet IN407

class Paquet:
    nombre_paquets = 0
    def __init__(self,source=0):
        Paquet.nombre_paquets += 1
        self.valeur = Paquet.nombre_paquets+1
        self.source = source

    def __repr__(self):
        return str(self.valeur)

class Buffer:
    nombre_buffers = 0
    Capacité = 100 
    def __init__(self,successeur=None):
        # L'idée derrière prédescesseur et successeur est de lier les buffer entre eux, mais aussi à leur Source notamment pour simplifier la transmission des paquets
        # Remarque : un buffer peut avoir plusieurs prédescesseurs 
        Buffer.nombre_buffers += 1
        predecesseur=[]
        self.predecesseur = predecesseur
        self.successeur = successeur
        liste_attente = []
        self.liste_attente = liste_attente
        capacite_locale = 0
        self.capacite_locale = capacite_locale

    def Insertion(self,paquet:'Paquet'):
        if self.capacite_locale < Buffer.Capacité:
            self.liste_attente.append(paquet)
            self.capacite_locale += 1

    def Transmission(self):
        assert len(self.liste_attente) != 0, "Le Buffer est vide, il ne peut donc pas transmettre de paquet."
        if isinstance(self.successeur, Buffer):
            self.successeur.Insertion(paquet=self.liste_attente.pop(0)) 
            self.capacite_locale -= 1     

    def Update_Transmission(self):
        self.Transmission()

class Source(Buffer):
    nombre_sources = 0
    def __init__(self,Successeur_2:None): ####### Successeur_2 serait le buffer principal
        super().__init__(Successeur_2)  # Héritage -> chaque source à son propre Buffer intégré
        Source.nombre_sources += 1
        numéro = Source.nombre_sources # On initialise le numéro de la source
        self.numéro = numéro
        active = True
        self.active = active
        fournit = []  # sauvegarde des paquets générés
        self.fournit = fournit
        temps = 0
        self.temps = temps

    def Generateur_paquet(self):
        # Générateur de paquet !!!! Attention il ne respecte pas encore la loi de poisson ---- a vérifier 
        from random import randint
        import time
        temps_delta = randint(1,5)
        self.temps += temps_delta
        time.sleep(temps_delta)  ##################### cela implique d'utiliser des threads lors de l'éxécution de la fonction afin de ne pas arrêter tous le script 
        paquet = Paquet(source=self.numéro)
        print(f"paquet n°{paquet} provenant de {self.numéro} - temps : {self.temps}")
        self.fournit.append(paquet)
        self.Insertion(paquet)   
                                             
    def Update(self):
        if self.active == True:
            self.Generateur_paquet()
                           
class Stratégie:
    # Cette classe à pour but d'encapsuler les stratégies de flux de données et d'encapsuler les quelques variables nécessaires au déroulement du script (a priori environ 5)
    def __init__(self,numéro):
        assert numéro in [1,2,3], "Il n'existe que 3 stratégie différente."
        Destination = Buffer() ; Destination.capacite_locale = 80 # On aggrandit la capacité locale de Destination en l'initialisant à -1000 au lieu de 0 pour les autres objets
        self.Destination = Destination
        if numéro == 1:
            # Implémentation de la stratégie n°1
            Buffer_Principal = Buffer(Destination)
            SourceA = Source(Successeur_2=Buffer_Principal)
            SourceB = Source(Successeur_2=Buffer_Principal)
            Buffer_Principal.predecesseur = [SourceA,SourceB]
            ############### Utilisation de Thread pour lancer l'éxécution de la génération de paquet, un tube de communication pourrait aussi être nécessaire.
            # Pour l'instant j'essaie de mettre en place une implémentation simple, sans parallélisme de procéssus pour tester préalablement les classes.
            SourceA.Generateur_paquet() ; SourceB.Generateur_paquet()
            test = 0
            while Destination.capacite_locale < Buffer.Capacité:
                test += 1
                SourceA.Update() ; SourceB.Update()
                print(f"Buffer Principal : {Buffer_Principal.liste_attente}")
                print(f"Buffer Destination : {Destination.liste_attente}")
                if SourceA.capacite_locale > SourceB.capacite_locale:
                    SourceA.Transmission()
                else:
                    SourceB.Transmission()

                if test > 5:
                    Buffer_Principal.Update_Transmission() ; Destination.Update_Transmission()

            SourceA.active = False ; SourceB.active = False
            print(SourceA.liste_attente)

Test = Stratégie(1)