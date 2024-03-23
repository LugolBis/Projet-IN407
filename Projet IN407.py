### Projet IN407 

class Paquet:
    nombre_paquets = 0
    def __init__(self,source=0):
        Paquet.nombre_paquets += 1
        poids = 1.5
        self.valeur = Paquet.nombre_paquets
        self.source = source
        self.poids = poids

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

    def Update_Transmission(self,temps=0):
        import time
        time.sleep(temps)  ### Introduction de la notion de débit pour le Buffer principal 
        if self.capacite_locale>0:
            self.Transmission()

class Source(Buffer):
    nombre_sources = 0
    def __init__(self,successeur=None): # successeur est le buffer principal
        super().__init__(successeur)  # Héritage -> chaque source à son propre Buffer intégré
        Source.nombre_sources += 1
        numéro = Source.nombre_sources # On initialise le numéro de la source
        self.numéro = numéro
        import time 
        time_active = time.time()
        self.tmps = time_active
        active = True 
        self.active = active
        fournit = []  # sauvegarde des paquets générés
        self.fournit = fournit

    def Generateur_paquet(self):
        # Générateur de paquet !!!! Attention il ne respecte pas encore la loi de poisson ---- a vérifier 
        assert isinstance(self.successeur, Buffer), f"La source n°{self.numéro} n'a pas de successeur valide."
        from random import randint
        import time
        temps_delta = randint(1,2)
        time.sleep(temps_delta)  ##################### cela implique d'utiliser des threads lors de l'éxécution de la fonction afin de ne pas arrêter tous le script 
        paquet = Paquet(source=self.numéro)
        print(f"paquet n°{paquet} provenant de {self.numéro} -- temps d'attente : {temps_delta} -- temps actuel : {time.time()-self.tmps} -- temps initial : {self.tmps}")
        self.fournit.append(paquet)
        self.Insertion(paquet)   
                                             
    def Update(self):
        if self.active == True:
            self.Generateur_paquet()
                           
class Stratégie:
    # Cette classe à pour but d'encapsuler les stratégies de gestion de flux de données et d'encapsuler les quelques variables nécessaires au déroulement du script (a priori environ 5)
    def __init__(self,numéro):
        assert numéro in [1,2,3], "Il n'existe que 3 stratégie différente qui sont [1,2,3]."
        Destination = Buffer() ; Destination.capacite_locale = 80 # On aggrandit la capacité locale de Destination en l'initialisant à -1000 au lieu de 0 pour les autres objets
        self.Destination = Destination
        # Initialisation des objets    -- Si plus de deux sources sont nécessaires c'est ici qu'il faudra créer les objets 
        Buffer_Principal = Buffer(Destination)
        SourceA = Source(Buffer_Principal)
        SourceB = Source(Buffer_Principal)
        Buffer_Principal.predecesseur = [SourceA,SourceB]

        if numéro == 1:
            # Implémentation de la stratégie n°1
            ############### Utilisation de Thread pour lancer l'éxécution de la génération de paquet, un tube de communication pourrait aussi être nécessaire.
            # Pour l'instant j'essaie de mettre en place une implémentation simple, sans parallélisme de procéssus pour tester préalablement les classes.
            SourceA.Generateur_paquet() ; SourceB.Generateur_paquet() 

            while Destination.capacite_locale < Buffer.Capacité:            
                SourceA.Update() ; SourceB.Update()                           

                if SourceA.capacite_locale > SourceB.capacite_locale:         
                    SourceA.Update_Transmission()
                else:
                    SourceB.Update_Transmission()

                Buffer_Principal.Update_Transmission() ; Destination.Update_Transmission()

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.liste_attente}")
                print(f"Buffer Destination : {Destination.liste_attente}")
                print(f"Liste_attente SourceA : {SourceA.liste_attente} -- Buffer Source A : {SourceA.successeur.liste_attente} -- Paquets fournit par la SourceA : {SourceA.fournit}")
                print(f"Liste_attente SourceB : {SourceB.liste_attente} -- Buffer Source B : {SourceB.successeur.liste_attente} -- Paquets fournit par la SourceB : {SourceB.fournit}")
                print(f"\n")

            SourceA.active = False ; SourceB.active = False
            print("Fin du test !")
        
        elif numéro == 2:
            # Implémentation de la stratégie n°2
            ############### Utilisation de Thread pour lancer l'éxécution de la génération de paquet, un tube de communication pourrait aussi être nécessaire.
            # Pour l'instant j'essaie de mettre en place une implémentation simple, sans parallélisme de procéssus pour tester préalablement les classes.
            SourceA.Generateur_paquet() ; SourceB.Generateur_paquet() 
            alternance = 0  # On fait alterner la source choisit par le Buffer principal 

            while Destination.capacite_locale < Buffer.Capacité:            
                SourceA.Update() ; SourceB.Update()                           

                if alternance == 0:         
                    SourceA.Update_Transmission()
                    alternance = 1
                else:
                    SourceB.Update_Transmission()
                    alternance = 0

                Buffer_Principal.Update_Transmission() ; Destination.Update_Transmission()

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.liste_attente}")
                print(f"Buffer Destination : {Destination.liste_attente}")
                print(f"Liste_attente SourceA : {SourceA.liste_attente} -- Buffer Source A : {SourceA.successeur.liste_attente} -- Paquets fournit par la SourceA : {SourceA.fournit}")
                print(f"Liste_attente SourceB : {SourceB.liste_attente} -- Buffer Source B : {SourceB.successeur.liste_attente} -- Paquets fournit par la SourceB : {SourceB.fournit}")
                print(f"\n")

            SourceA.active = False ; SourceB.active = False
            print("Fin du test !")

        elif numéro == 3:
            # Implémentation de la stratégie n°3
            ############### Utilisation de Thread pour lancer l'éxécution de la génération de paquet, un tube de communication pourrait aussi être nécessaire.
            # Pour l'instant j'essaie de mettre en place une implémentation simple, sans parallélisme de procéssus pour tester préalablement les classes.
            SourceA.Generateur_paquet() ; SourceB.Generateur_paquet() 
            from random import randint ; alternance = randint(0,1)  # On fait alterner la source choisit par le Buffer principal 
            
            while Destination.capacite_locale < Buffer.Capacité:            
                SourceA.Update() ; SourceB.Update()                           

                if alternance == 0:         
                    SourceA.Update_Transmission()
                    alternance = randint(0,1)
                else:
                    SourceB.Update_Transmission()
                    alternance = randint(0,1)

                Buffer_Principal.Update_Transmission() ; Destination.Update_Transmission()

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.liste_attente}")
                print(f"Buffer Destination : {Destination.liste_attente}")
                print(f"Liste_attente SourceA : {SourceA.liste_attente} -- Buffer Source A : {SourceA.successeur.liste_attente} -- Paquets fournit par la SourceA : {SourceA.fournit}")
                print(f"Liste_attente SourceB : {SourceB.liste_attente} -- Buffer Source B : {SourceB.successeur.liste_attente} -- Paquets fournit par la SourceB : {SourceB.fournit}")
                print(f"\n")

            SourceA.active = False ; SourceB.active = False
            print("Fin du test !")

Test = Stratégie(1)



# Note 1 : La classe Stratégie est pour l'heure implémentée en partant du principe qu'il n'y a que deux sources générant des paquets, 
#            augmenter le nombre de source de manière automatique à partir d'un entier serait possible avec la fonction : 'globals()[nom_variable] = valeur_variable'

# Note 2 : La classe Stratégie est pour l'heure particulièrement incomplète car elle ne fournit aucun élément d'appel des sources/buffer quelle génère
#          Cela risque notamment de poser problème pour l'analyse de la perte de paquet et du temps moyen d'attente  

# Note 3 : La notion de thread n'a pas encore été introduite et risque de poser de nompbreux problèmes...     