### Projet IN407

class Paquet:
    nombre_paquets = 0
    def __init__(self,source=0,valeur=1.5):
        Paquet.nombre_paquets += 1
        self.valeur = valeur
        self.source = source

class Buffer:
    nombre_buffers = 0
    Capacité = 100 
    def __init__(self,predecesseur=None,successeur=None):
        # L'idée derrière prédescesseur et successeur est de lier les buffer entre eux, mais aussi à leur Source notamment pour simplifier la transmission des paquets
        # Remarque : un buffer peut avoir plusieurs prédescesseurs 
        Buffer.nombre_buffers += 1
        self.predecesseur = predecesseur
        self.successeur = successeur
        liste_attente = []
        self.liste_attente = liste_attente
        capacite_locale = len(liste_attente)
        self.capacite_locale = capacite_locale

    def Insertion(self,paquet:'Paquet'):
        if self.capacite_locale < Buffer.Capacité:
            self.liste_attente.append(paquet)

    def Transmission(self,paquet:'Paquet'):
        ######### Il n'y a pour l'instant aucune contrainte de temps et de débit. Chose à rajouter après.
        assert len(self.liste_attente) != 0, "Le Buffer est vide, il ne peut donc pas transmettre de paquet."
        if isinstance(self.successeur, Buffer):
            self.successeur.Insertion(paquet=self.liste_attente.pop(0))      

class Source:
    nombre_sources = 0
    def __init__(self,Successeur_2:None): ####### Successeur_2 serait le buffer principal
        Buffer.__init__(self,successeur=Successeur_2)  # Héritage 
        Source.nombre_sources += 1
        numéro = Source.nombre_sources # On initialise le numéro de la source
        self.numéro = numéro
        active = True
        self.active = active

    def Generateur_paquet(self):
        # Générateur de paquet !!!! Attention il ne respecte pas encore la loi de poisson ---- a vérifier 
        from random import randint
        import time
        temps = 0
        while self.active == True:
            temps_delta = randint(1,10)
            temps += temps_delta
            time.sleep(temps_delta)  ##################### cela implique d'utiliser des threads lors de l'éxécution de la fonction afin de ne pas arrêter tous le script 
            self.Insertion(Paquet(source=self.numéro))   
                                             
    def Stop_generateur_paquet(self):
        self.active = False # C'est une première idée certainement maladroite et inadaptée aux threads, il serait sûrement plus simple de mettre fin au thread dans lequel 'Generateur_paquet()' à été lancé
                            # Ou il faudrait que cette fonction soit lancée dans le même ""espace mémoire"" que le thread de la fonction 'Generateur_paquet()' --> ou utiliser la communication entre les processus
        
class Stratégie:
    # Cette classe à pour but d'encapsuler les stratégies de flux de données et d'encapsuler les quelques variables nécessaires au déroulement du script (a priori environ 5)
    def __init__(self,numéro):
        self.numéro = numéro # Le huméro sera utilisé pour différencier les 3 stratégies différentes