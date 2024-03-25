### Projet IN407 

class Paquet:
    nombre_paquets = 0
    def __init__(self,source=0):
        Paquet.nombre_paquets += 1 # On compte au fur et à mesure le nombre de paquet créés 
        poids = 1.5   # On initialise par défaut le poids à 1,5 étant donné qu'il n'est pas obligatoire de s'en préoccuper
        
        self.valeur = Paquet.nombre_paquets  # Chaque paquet est différencié par sa valeur, qui est simplement le n° du n-ième paquet
        self.source = source
        self.poids = poids 

    def __repr__(self):
        return str(self.valeur)  # Chaque paquet est simplement représenté par sa valeur 

class Buffer:
    nombre_buffers = 0  # Cette variable de classe permet de compter le nombre de Buffer 
    Capacité = 100   # Cette variable de classe initialise la capacité maximale d'un Buffer (donc 100 paquet pour l'heure)
    def __init__(self,successeur=None):
        # L'idée derrière prédescesseur et successeur est de lier les buffer entre eux, mais aussi à leur Source notamment pour simplifier la transmission des paquets
        # Remarque : un buffer peut avoir plusieurs prédescesseurs 
        Buffer.nombre_buffers += 1 # On incrémente la variable de classe comptant le nombre de buffer dès la création d'un nouveau buffer 
        predecesseur=[]  # On peut ici stocker les prédecesseurs du Buffer, ce qui pourra servir plus tard pour l'interface graphique
        self._predecesseur = predecesseur

        liste_attente = []  # On initialise le coeur du Buffer sous la forme d'une liste, les paquets transmis au Buffer seront stockés ici 
        self._liste_attente = liste_attente

        capacite_locale = 0  # On initialise la capacité locale du Buffer
        self._capacite_locale = capacite_locale

        self._successeur = successeur # Bien sûr on initialise une méthode permetant d'accéder au successeur du Buffer
        
    def getPredecesseur(self):
        return self._predecesseur
    def setPredecesseur(self,nouvelle_valeur=None):
        if nouvelle_valeur != None:
            self._predecesseur = nouvelle_valeur

    def getListe_attente(self):
        return self._liste_attente
    def setListe_attente(self,element):
        """L'élément en entrée doit être un tuple (OPCODE,Variable) tel que:
        - l'OPCODE indique l'opération à effectuer : ['ECRASE','AJOUT','DEPOP']
        - la Variable est l'objet en lui même \n
        'ECRASE' -> écrase la liste par la liste en entrée \n
        'AJOUT' -> ajoute l'objet à la liste \n
        'DEPOP' -> on renvoie l'élément que l'on à dépop de la liste à l'indice de la Variable"""
        OPCODE = element[0]
        Variable = element[1]
        if OPCODE == "ECRASE":
            self._liste_attente = Variable
        elif OPCODE == "AJOUT" :
            self._liste_attente.append(Variable)
        elif OPCODE == "DEPOP":
            return self._liste_attente.pop(Variable)

    def getCapacite_locale(self):
        return self._capacite_locale
    def setCapacite_locale(self,ajout=0):
        self._capacite_locale += ajout

    def getSuccesseur(self):
        return self._successeur
    def setSuccesseur(self,buffer:'Buffer'):
        assert isinstance(buffer,[Buffer,list]), "Le successeur d'un buffer doit être un Buffer ou une liste."
        self._successeur = buffer

    predecesseur = property(getPredecesseur, setPredecesseur)
    liste_attente = property(getListe_attente,setListe_attente)
    capacite_locale = property(getCapacite_locale,setCapacite_locale)
    successeur = property(getSuccesseur,setSuccesseur)

    def Insertion(self,paquet:'Paquet'):
        """ Cette méthode permet d'insérer un Paquet dans le buffer """ 
        if self.capacite_locale < Buffer.Capacité: # On s'assure ici que le buffer n'est pas déjà plein
            #self.liste_attente.append(paquet)
            self.setListe_attente(('AJOUT',paquet))
            self.setCapacite_locale(ajout=1)

    def Transmission(self,temps=0):
        """ Cette méthode permet de transmettre un paquet au buffer successeur du buffer avec lequel cette méthode est appelé \n
        En résumé : bufferA [Paquet1,Paquet2,...,PaquetN] et bufferB [ ] -> bufferA [Paquet2,...,PaquetN] et bufferB [Paquet1] """ 
        import time
        #assert len(self.liste_attente) != 0, "Le Buffer est vide, il ne peut donc pas transmettre de paquet."
        time.sleep(temps)
        if isinstance(self.getSuccesseur(), Buffer) and (self.getCapacite_locale()>0): # On s'assure que le successeur est bien un objet de type 'Buffer' et que le buffer ""source"" n'est pas vide
            self.getSuccesseur().Insertion(paquet=self.setListe_attente(('DEPOP',0))) # On insère dans le buffer successeur le premier paquet du buffer 
            self.setCapacite_locale(ajout = -1)     

class Source(Buffer):
    nombre_sources = 0
    liste_sources = [] # On stock dans une variable de la classe tous les objets 'Source'
    def __init__(self,successeur=None): # successeur est le buffer principal
        super().__init__(successeur)  # Héritage -> chaque source à son propre Buffer intégré
        Source.nombre_sources += 1
        numéro = Source.nombre_sources # On initialise le numéro de la source
        Source.liste_sources.append(self) # On ajoute à la variable de classe la Source en elle même 
        self._numéro = numéro
        import time 
        time_active = time.time() # On initialise le temps de création de la source -> notamment utilisé
        self._time_active = time_active
        active = True 
        self._active = active
        fournit = []  # Liste permettant la sauvegarde de tous les paquets générés -> sera utile pour les taux de pertes 
        self._fournit = fournit

    def getNuméro(self):
        return self._numéro
    def setNuméro(self,nouveau_numéro=0):   # On utilisira jamais cette fonction ! Elle est là pour décorer.
        self._numéro = nouveau_numéro

    def getTime_active(self):
        return self._time_active
    def setTime_active(self,nouveau_temps=0):
        self._time_active = nouveau_temps

    def getActive(self):
        return self._active
    def setActive(self,état=True):
        """L'état doit être l'une des valeurs : 
        - Tue
        - False"""
        self._active = état

    def getFournit(self):
        return self._fournit
    def setFournit(self,ajout):
        self._fournit.append(ajout)   

    numéro = property(getNuméro,setNuméro)
    time_active = property(getTime_active,setTime_active)
    active = property(getActive,setActive)
    fournit = property(getFournit,setFournit)

    def Generateur_paquet(self):
        """ Générateur de paquet -- Attention !!!! il ne respecte pas encore la loi de poisson"""
        assert isinstance(self.getSuccesseur(), Buffer), f"La source n°{self.getNuméro()} n'a pas de successeur valide."
        from random import randint
        import time
        if self.getActive() == True:
            temps_delta = randint(1,2) # On choisit le délait d'attente avant de générer un nouveau paquet 
            time.sleep(temps_delta)  ##################### cela implique d'utiliser des threads lors de l'éxécution de la fonction afin de ne pas arrêter tous le script 
            paquet = Paquet(source=self.getNuméro()) # On génère un paquet 
            print(f"paquet n°{paquet} provenant de {self.getNuméro()} -- temps d'attente : {temps_delta} -- temps actuel : {time.time()-self.getTime_active()} -- temps initial : {self.getTime_active()}")
            self.setFournit(ajout=paquet)
            self.Insertion(paquet) # On insère le paquet directement dans le Buffer rataché à la source 

    def AfficheTest(self):
        """ Cette fonction est temporaire elle ne sert qu'à afficher l'évolution de la Source pour faciliter les tests sur la classe """
        print(f"Liste_attente Source {self.getNuméro()} : {self.getListe_attente()} -- Buffer Source {self.getNuméro()} : {self.getSuccesseur().getListe_attente()} -- Paquets fournit par la Source {self.getNuméro()} : {self.getFournit()}")
                           
class Stratégie:
    # Cette classe à pour but d'encapsuler les stratégies de gestion de flux de données et d'encapsuler les quelques variables nécessaires au déroulement du script (a priori environ 5)
    def __init__(self,numéro,nombre_source=2,échantillon=20):
        assert numéro in [1,2,3], "Il n'existe que 3 stratégie différente qui sont : [1,2,3]."
        assert isinstance(nombre_source,int), "Le nombre de sources utilisées dans la simulation doit être un entier."
        Destination = Buffer() 
        Destination.setCapacite_locale(ajout=Buffer.Capacité - échantillon)  # On initialise la capacité local du Buffer Destination pour décider de la taille de l'échantillon de paquets nous allons baser nos analyses
        self.Destination = Destination

        # Initialisation des objets
        Buffer_Principal = Buffer(Destination) # On initialise le Buffer principal 
        for s in range(nombre_source):   # A chaque itération on crée un objet source, qui sera directement stocké dans 'Source.liste_sources' lors de l'initialisation de ceux-ci
            Source(Buffer_Principal)
        Buffer_Principal.setPredecesseur(Source.liste_sources) 

        if numéro == 1:
            # Implémentation de la stratégie n°1
            ############### Utilisation de Thread pour lancer l'éxécution de la génération de paquet, un tube de communication pourrait aussi être nécessaire.
            # Pour l'instant j'essaie de mettre en place une implémentation simple, sans parallélisme de procéssus pour tester préalablement les classes.
            for source_ in Source.liste_sources :
                source_.Generateur_paquet() 

            while Destination.getCapacite_locale() < Buffer.Capacité:            
                for source_ in Source.liste_sources : 
                    source_.Generateur_paquet()          # On fait une update sur toutes les sources (cela génère des paquets en résumé)         

                source_Transmission = None # On initialise la source dont on va transmettre un paquet à None
                capacite_max = 0 # On initialise la capacité locale de la source transmission à 0
                for source_ in Source.liste_sources :
                    if source_.getCapacite_locale() > capacite_max:  # On choisit ici la source_ dont la capacite locale est maximale 
                        capacite_max = source_.getCapacite_locale()
                        source_Transmission = source_
                source_Transmission.Transmission()  # On lance le processus de tranmsission de la source choisit en amont vers le Buffer principal

                Buffer_Principal.Transmission() ; Destination.Transmission()

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.getListe_attente()}")
                print(f"Buffer Destination : {Destination.getListe_attente()}") 
                for source_ in Source.liste_sources : 
                    source_.AfficheTest()
                print(f"\n")

            for source_ in Source.liste_sources : 
                    source_.setActive(False)
            print("Fin du test !")
        
        elif numéro == 2:
            # Implémentation de la stratégie n°2
            ############### Utilisation de Thread pour lancer l'éxécution de la génération de paquet, un tube de communication pourrait aussi être nécessaire.
            # Pour l'instant j'essaie de mettre en place une implémentation simple, sans parallélisme de procéssus pour tester préalablement les classes.
            for source_ in Source.liste_sources :
                source_.Generateur_paquet() 
            file_attente = Source.liste_sources  # On initialise une source d'attente qui sera utilisée pour faire alterner le choix de la source par le Buffer principal

            while Destination.getCapacite_locale() < Buffer.Capacité:            
                for source_ in Source.liste_sources :
                    source_.Generateur_paquet()                            

                source_ = file_attente.pop(0) # On retire le premier élément de la file d'attente des sources
                source_.Transmission() # On traite la source
                file_attente.append(source_) # On remet la source dans la file d'attente 

                Buffer_Principal.Transmission() ; Destination.Transmission()

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.getListe_attente()}")
                print(f"Buffer Destination : {Destination.getListe_attente()}")
                for source_ in Source.liste_sources : 
                    source_.AfficheTest()
                print(f"\n")

            for source_ in Source.liste_sources : 
                    source_.setActive(False)
            print("Fin du test !")

        elif numéro == 3:
            # Implémentation de la stratégie n°3
            ############### Utilisation de Thread pour lancer l'éxécution de la génération de paquet, un tube de communication pourrait aussi être nécessaire.
            # Pour l'instant j'essaie de mettre en place une implémentation simple, sans parallélisme de procéssus pour tester préalablement les classes.
            for source_ in Source.liste_sources :
                source_.Generateur_paquet() 
            from random import randint 
            file_attente = Source.liste_sources  # On initialise une source d'attente qui sera utilisée pour faire alterner le choix de la source par le Buffer principal 
            indice_max = len(file_attente)-1 # On initialise l'indice max pouvant être tiré au hasard pour accéder à la file d'attente 
            
            while Destination.getCapacite_locale() < Buffer.Capacité:            
                for source_ in Source.liste_sources :
                    source_.Generateur_paquet()                            

                source_ = file_attente[randint(0,indice_max)]  # On prend aléatoirement une source dans la file d'attente 
                source_.Transmission()     # On traite la source

                Buffer_Principal.Transmission() ; Destination.Transmission()

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.getListe_attente()}")
                print(f"Buffer Destination : {Destination.getListe_attente()}")
                for source_ in Source.liste_sources : 
                    source_.AfficheTest()
                print(f"\n")

            for source_ in Source.liste_sources : 
                    source_.setActive(False) 
            print("Fin du test !")

Test = Stratégie(1,2)


# Note 1 : La classe Stratégie est pour l'heure particulièrement incomplète car elle ne fournit aucun élément d'appel des sources/buffer quelle génère
#          Cela risque notamment de poser problème pour l'analyse de la perte de paquet et du temps moyen d'attente  

# Note 2 : La notion de thread n'a pas encore été introduite et risque de poser de nompbreux problèmes...  