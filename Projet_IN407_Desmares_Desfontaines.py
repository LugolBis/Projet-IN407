### Projet IN407 

import time
import random
import threading

class Paquet:
    nombre_paquets = 0
    def __init__(self,source=0):
        Paquet.nombre_paquets += 1 # On compte au fur et à mesure le nombre de paquet créés 
        poids = 1.5   # On initialise par défaut le poids à 1,5 étant donné qu'il n'est pas obligatoire de s'en préoccuper
        
        self.valeur = Paquet.nombre_paquets  # Chaque paquet est différencié par sa valeur, qui est simplement le n° du n-ième paquet
        self.source = source
        self.poids = poids 
        
        temps_émission = time.time()  # On initialise le temps auquel le paquet est généré 
        self._temps_émision = temps_émission 

        temps_arrivé = None  # On initialise le temps d'arrivé a destination du paquet 
        self._temps_arrivé = temps_arrivé 

    def getTemps_émission(self):
        return self._temps_émision
    def setTemps_émission(self,nouveau_temps=None):
        """Il est fortement conseillé de passer 'time.time()' en argument de 'nouveau_temps'."""
        self._temps_émision = nouveau_temps 

    def getTemps_arrivé(self):
        return self._temps_arrivé
    def setTemps_arrivé(self,nouveau_temps=None):
        """Il est fortement conseillé de passer 'time.time()' en argument de 'nouveau_temps'."""
        self._temps_arrivé = nouveau_temps
    
    temps_émision = property(getTemps_émission, setTemps_émission)
    temps_arrivé = property(getTemps_arrivé, setTemps_arrivé)
    
    def Calcule_attente(self):
        """Cette méthode renvoie le temps d'attente du paquet entre son émission et son arrivée dans à Destination."""
        return self.getTemps_arrivé() - self.getTemps_émission()

    def __repr__(self):
        return str(self.valeur)  # Chaque paquet est simplement représenté par sa valeur 

class Buffer:
    nombre_buffers = 0  # Cette variable de classe permet de compter le nombre de Buffer 
    Capacité = 100   # Cette variable de classe initialise la capacité maximale d'un Buffer (donc 100 paquet pour l'heure)
    liste_buffers = []
    def __init__(self,successeur=None):
        # L'idée derrière prédescesseur et successeur est de lier les buffer entre eux, mais aussi à leur Source notamment pour simplifier la transmission des paquets
        # Remarque : un buffer peut avoir plusieurs prédescesseurs 
        Buffer.nombre_buffers += 1 # On incrémente la variable de classe comptant le nombre de buffer dès la création d'un nouveau buffer 
        Buffer.liste_buffers.append(self) # On ajoute à la variable de classe le Buffer en lui même
        predecesseur=[]  # On peut ici stocker les prédecesseurs du Buffer, ce qui pourra servir plus tard pour l'interface graphique
        self._predecesseur = predecesseur

        liste_attente = []  # On initialise le coeur du Buffer sous la forme d'une liste, les paquets transmis au Buffer seront stockés ici 
        self._liste_attente = liste_attente

        capacite_locale = 0  # On initialise la capacité locale du Buffer
        self._capacite_locale = capacite_locale

        self._successeur = successeur # Bien sûr on initialise une méthode permetant d'accéder au successeur du Buffer

        active = True  # On initialise une variable active pour contrôler l'activité du Buffer 
        self._active = active 
        
    def getPredecesseur(self):
        return self._predecesseur
    def setPredecesseur(self,nouvelle_valeur=None):
        if nouvelle_valeur != None:
            self._predecesseur = nouvelle_valeur

    def getListe_attente(self):
        return self._liste_attente
    def setListe_attente(self,element):
        """L'élément en entrée doit être un tuple (OPCODE,Variable) tel que :
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

    def getActive(self):
        return self._active
    def setActive(self,état):
        assert état in [True,False], "La variable état ne prend que les valeurs : True, False."
        self._active = état

    predecesseur = property(getPredecesseur, setPredecesseur)
    liste_attente = property(getListe_attente,setListe_attente)
    capacite_locale = property(getCapacite_locale,setCapacite_locale)
    successeur = property(getSuccesseur,setSuccesseur)
    active = property(getActive,setActive)

    def Insertion(self,paquet:'Paquet'):
        """ Cette méthode permet d'insérer un Paquet dans le buffer """ 
        if self.capacite_locale < Buffer.Capacité: # On s'assure ici que le buffer n'est pas déjà plein
            #self.liste_attente.append(paquet)
            self.setListe_attente(('AJOUT',paquet))
            self.setCapacite_locale(ajout=1)

    def Transmission(self,débit=0):
        """ Cette méthode permet de transmettre un paquet au buffer successeur du buffer avec lequel cette méthode est appelé \n
        En résumé : bufferA [Paquet1,Paquet2,...,PaquetN] et bufferB [ ] -> bufferA [Paquet2,...,PaquetN] et bufferB [Paquet1] """ 
        time.sleep(débit) # On fait attendre le Buffer pour simuler son débit
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
        """L'état doit être l'une des valeurs : \n - True  \n - False"""
        self._active = état

    def getFournit(self):
        return self._fournit
    def setFournit(self,ajout):
        self._fournit.append(ajout)   

    numéro = property(getNuméro,setNuméro)
    time_active = property(getTime_active,setTime_active)
    active = property(getActive,setActive)
    fournit = property(getFournit,setFournit)

    def Generateur_paquet(self,lambda_poisson=0.5):
        """ Générateur de paquet -- Attention !!!! il ne respecte pas encore la loi de poisson"""
        assert isinstance(self.getSuccesseur(), Buffer), f"La source n°{self.getNuméro()} n'a pas de successeur valide."
        if self.getActive() == True :
            temps_delta = random.expovariate(1/lambda_poisson) # On choisit le délait d'attente avant de générer un nouveau paquet 
            time.sleep(temps_delta) 
            paquet = Paquet(source=self.getNuméro()) # On génère un paquet 
            print(f"paquet n°{paquet} provenant de {self.getNuméro()} -- temps d'attente : {temps_delta} -- temps actuel : {time.time()-self.getTime_active()} -- temps initial : {self.getTime_active()}")
            self.setFournit(ajout=paquet)
            self.Insertion(paquet) # On insère le paquet directement dans le Buffer rataché à la source 

    def AfficheTest(self):
        """ Cette fonction est temporaire elle ne sert qu'à afficher l'évolution de la Source pour faciliter les tests sur la classe """
        print(f"Buffer Source {self.getNuméro()} : {self.getListe_attente()} -- Paquets fournit par la Source {self.getNuméro()} : {self.getFournit()}")

class Stratégie:
    # Cette classe à pour but d'encapsuler les stratégies de gestion de flux de données et d'encapsuler les quelques variables nécessaires au déroulement du script (a priori environ 5)
    def __init__(self,numéro,nombre_source=2,échantillon=20,parametre_poisson=0.5):
        assert numéro in [1,2,3,4], "Il n'existe que 3 stratégie différente qui sont : [1,2,3]."
        assert isinstance(nombre_source,int), "Le nombre de sources utilisées dans la simulation doit être un entier."
        Destination = Buffer() 
        Destination.setCapacite_locale(ajout=Buffer.Capacité - échantillon)  # On initialise la capacité local du Buffer Destination pour décider de la taille de l'échantillon de paquets nous allons baser nos analyses
        self.Destination = Destination
        DEBUT_TEMPS_TEST = time.time()

        # Initialisation des objets
        Buffer_Principal = Buffer(Destination) # On initialise le Buffer principal 
        for s in range(nombre_source):   # A chaque itération on crée un objet source, qui sera directement stocké dans 'Source.liste_sources' lors de l'initialisation de ceux-ci
            Source(Buffer_Principal)
        Buffer_Principal.setPredecesseur(Source.liste_sources) 

        if numéro == 1:
            # Implémentation de la stratégie n°1
            for source_ in Source.liste_sources :
                source_.Generateur_paquet(parametre_poisson) 

            while Destination.getCapacite_locale() < Buffer.Capacité: 
                
                liste_threads = []    # On initialise la liste des threads qui vont être éxécutés durant la boucle

                liste_threads.append(threading.Thread(target=Buffer_Principal.Transmission(), args=(1,5)))
                liste_threads[0].start() # On démarre la transmission du Buffer Principal 

                for source_ in Source.liste_sources : 
                    liste_threads.append(threading.Thread(target=source_.Generateur_paquet(), args=(parametre_poisson,)))          # On fait une update sur toutes les sources (cela génère des paquets en résumé)         

                for thread in liste_threads[1:]:
                    thread.start()

                for thread in liste_threads[1:]:
                    thread.join()

                source_Transmission = None # On initialise la source dont on va transmettre un paquet à None
                capacite_max = 0 # On initialise la capacité locale de la source transmission à 0
                for source_ in Source.liste_sources :
                    if source_.getCapacite_locale() > capacite_max:  # On choisit ici la source_ dont la capacite locale est maximale 
                        capacite_max = source_.getCapacite_locale()
                        source_Transmission = source_

                liste_threads.append(threading.Thread(target=source_Transmission.Transmission()))  # On lance le thread de tranmsission de la source choisit en amont vers le Buffer principal
                liste_threads[-1].start()
                liste_threads[-1].join()

                liste_threads[0].join() # Destination.Transmission()

                if Destination.getListe_attente() != []:
                    Destination.getListe_attente()[-1].setTemps_arrivé(time.time()) # Dès qu'un paquet arrive on stock son temps d'arrivé

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.getListe_attente()}")
                print(f"Buffer Destination : {Destination.getListe_attente()}") 
                for source_ in Source.liste_sources : 
                    source_.AfficheTest()
                print(f"\n")

            for source_ in Source.liste_sources : 
                    source_.setActive(False)
            print(f"Fin du test !\n Le test a duré : {time.time() - DEBUT_TEMPS_TEST}")
        
        elif numéro == 2:
            # Implémentation de la stratégie n°2
            for source_ in Source.liste_sources :
                source_.Generateur_paquet(parametre_poisson) 
            file_attente = Source.liste_sources  # On initialise une file d'attente qui sera utilisée pour faire alterner le choix de la source par le Buffer principal

            while Destination.getCapacite_locale() < Buffer.Capacité:  

                liste_threads = []    # On initialise la liste des threads qui vont être éxécutés durant la boucle

                liste_threads.append(threading.Thread(target=Buffer_Principal.Transmission(), args=(1,5)))
                liste_threads[0].start() # On démarre la transmission du Buffer Principal 

                for source_ in Source.liste_sources : 
                    liste_threads.append(threading.Thread(target=source_.Generateur_paquet(), args=(parametre_poisson,)))          # On fait une update sur toutes les sources (cela génère des paquets en résumé)         

                for thread in liste_threads[1:]:
                    thread.start()

                for thread in liste_threads[1:]:
                    thread.join()                           

                source_Transmission = file_attente.pop(0) # On retire le premier élément de la file d'attente des sources
                liste_threads.append(threading.Thread(target=source_Transmission.Transmission()))  # On lance le thread de tranmsission de la source choisit en amont vers le Buffer principal
                liste_threads[-1].start()
                liste_threads[-1].join()
                file_attente.append(source_Transmission) # On remet la source dans la file d'attente                 

                liste_threads[0].join() # Destination.Transmission()

                if Destination.getListe_attente() != []:
                    Destination.getListe_attente()[-1].setTemps_arrivé(time.time()) # Dès qu'un paquet arrive on stock son temps d'arrivé

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.getListe_attente()}")
                print(f"Buffer Destination : {Destination.getListe_attente()}")
                for source_ in Source.liste_sources : 
                    source_.AfficheTest()
                print(f"\n")

            for source_ in Source.liste_sources : 
                    source_.setActive(False)
            print(f"Fin du test !\n Le test a duré : {time.time() - DEBUT_TEMPS_TEST}")

        elif numéro == 3:
            # Implémentation de la stratégie n°3
            for source_ in Source.liste_sources :
                source_.Generateur_paquet(parametre_poisson) 
            file_attente = Source.liste_sources  # On initialise une source d'attente qui sera utilisée pour faire alterner le choix de la source par le Buffer principal 
            indice_max = len(file_attente)-1 # On initialise l'indice max pouvant être tiré au hasard pour accéder à la file d'attente 
            
            while Destination.getCapacite_locale() < Buffer.Capacité: 

                liste_threads = []    # On initialise la liste des threads qui vont être éxécutés durant la boucle

                liste_threads.append(threading.Thread(target=Buffer_Principal.Transmission(), args=(1,5)))
                liste_threads[0].start() # On démarre la transmission du Buffer Principal 

                for source_ in Source.liste_sources : 
                    liste_threads.append(threading.Thread(target=source_.Generateur_paquet(),args=(parametre_poisson,)))  # On fait une update sur toutes les sources (cela génère des paquets en résumé)         

                for thread in liste_threads[1:]:
                    thread.start()

                for thread in liste_threads[1:]:
                    thread.join()                            

                source_Transmission = file_attente[random.randint(0,indice_max)]  # On prend aléatoirement une source dans la file d'attente 
                liste_threads.append(threading.Thread(target=source_Transmission.Transmission()))  # On lance le thread de tranmsission de la source choisit en amont vers le Buffer principal
                liste_threads[-1].start()
                liste_threads[-1].join()

                liste_threads[0].join()

                if Destination.getListe_attente() != []: 
                    Destination.getListe_attente()[-1].setTemps_arrivé(time.time()) # Dès qu'un paquet arrive on stock son temps d'arrivé 

                # Affichages de contôle pour s'assurer du bon fonctionnement du script 
                print(f"Buffer Principal : {Buffer_Principal.getListe_attente()}")
                print(f"Buffer Destination : {Destination.getListe_attente()}")
                for source_ in Source.liste_sources : 
                    source_.AfficheTest()
                print(f"\n")

            for source_ in Source.liste_sources : 
                    source_.setActive(False) 
            print(f"Fin du test !\n Le test a duré : {time.time() - DEBUT_TEMPS_TEST}")

    def Analyse_Temps(self):
        """Cette méthode renvoie le temps moyen d'attente des paquets contenu dans le 'Buffer_Destination' qui modélise le destinataire des paquets."""
        if isinstance(self.Destination, Buffer):
            Contenu = self.Destination.getListe_attente() # On récupère le Buffer_destination créé par le constructeur
            temps_attente = 0
            for paquet_ in Contenu :
                temps_attente += paquet_.Calcule_attente()
            return round(temps_attente/len(Contenu), 2)  # On renvoie un float arrondi à la 2ème décimale, contenant le temps moyen d'attente des paquets
        
    def Analyse_Taux(self):
        """Cette méthode calcule le taux de perte de paquets."""
        nombre_paquets_générés = Paquet.nombre_paquets # On récupère le nombre total de paquets générés
        nombre_paquets_stockés = 0
        for buffer_ in Buffer.liste_buffers :
            nombre_paquets_stockés += len(buffer_.getListe_attente()) # On ajoute le nombre de paquets stockés dans chaque buffer 
        résultat = round(nombre_paquets_stockés/nombre_paquets_générés, 2)  # On renvoie un float arrondi à la 2ème décimale, contenant le taux de perte des paquets
        if résultat == 1: 
            return 0.0
        else:
            return résultat

Test = Stratégie(1,2,20,0.5)

print("\n--------------------- Analyses ---------------------\n")
print(f"Le temps moyen d'attente des paquets est : {Test.Analyse_Temps()}")
print(f"Le taux de perte des paquets est : {Test.Analyse_Taux()}")

# Note 1 : La modélisation de la loi de poisson est aproximative 

# Note 2 : Y a pas d'interface graphique 

# Note 3 : Qu'en est il de la portabilité ?

class Interface:
    liste_objets = []
    def __init__(self):
        self.coucou = "Coucou Alexia ! Je te souhaites bon courage pour cette classe ;)"
