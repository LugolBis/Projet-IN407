### Projet IN407 

import time
import random
import threading
import customtkinter

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

        temps_arrivé = None  # On initialise le temps d'arrivé a sa destination du paquet 
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
    
    @classmethod
    def Réinitialiser(cls):
        Paquet.nombre_paquets = 0

    def __repr__(self):
        return str(self.valeur)  # Chaque paquet est simplement représenté par sa valeur 

class Buffer:
    nombre_buffers = 0  # Cette variable de classe permet de compter le nombre de Buffer 
    Capacité = 100   # Cette variable de classe initialise la capacité maximale d'un Buffer (donc 100 paquet pour l'heure)
    liste_buffers = []
    def __init__(self,successeur=None):
        # L'idée derrière prédescesseur et successeur est de lier les buffer entre eux, mais aussi à leur Source notamment pour simplifier la transmission des paquets
        # Remarque : un buffer peut avoir plusieurs prédecesseurs 
        Buffer.nombre_buffers += 1 # On incrémente la variable de classe comptant le nombre de buffer dès la création d'un nouveau buffer 
        Buffer.liste_buffers.append(self) # On ajoute à la variable de classe le Buffer en lui même
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

    def Transmission(self,débit=0):
        """ Cette méthode permet de transmettre un paquet au buffer successeur du buffer avec lequel cette méthode est appelé \n
        En résumé : bufferA [Paquet1,Paquet2,...,PaquetN] et bufferB [ ] -> bufferA [Paquet2,...,PaquetN] et bufferB [Paquet1] """ 
        time.sleep(débit) # On fait attendre le Buffer pour simuler son débit
        if isinstance(self.getSuccesseur(), Buffer) and (self.getCapacite_locale()>0): # On s'assure que le successeur est bien un objet de type 'Buffer' et que le buffer ""source"" n'est pas vide
            self.getSuccesseur().Insertion(paquet=self.setListe_attente(('DEPOP',0))) # On insère dans le buffer successeur le premier paquet du buffer 
            self.setCapacite_locale(ajout = -1) 

    @classmethod
    def Réinitialiser(cls):
        Buffer.nombre_buffers = 0  # Cette variable de classe permet de compter le nombre de Buffer 
        Buffer.Capacité = 100   # Cette variable de classe initialise la capacité maximale d'un Buffer (donc 100 paquet pour l'heure)
        Buffer.liste_buffers = []

class Source(Buffer):
    nombre_sources = 0
    liste_sources = [] # On stock dans une variable de la classe tous les objets 'Source'
    def __init__(self,successeur=None): # successeur est le buffer principal
        super().__init__(successeur)  # Héritage -> chaque source à son propre Buffer intégré
        Source.nombre_sources += 1
        numéro = Source.nombre_sources # On initialise le numéro de la source
        Source.liste_sources.append(self) # On ajoute à la variable de classe la Source en elle même 
        self._numéro = numéro

    def getNuméro(self):
        return self._numéro
    def setNuméro(self,nouveau_numéro=0):  
        self._numéro = nouveau_numéro

    numéro = property(getNuméro,setNuméro)

    def Generateur_paquet(self,lambda_poisson=0.5):
        """ Générateur de paquet"""
        assert isinstance(self.getSuccesseur(), Buffer), f"La source n°{self.getNuméro()} n'a pas de successeur valide."
        temps_delta = random.expovariate(1/lambda_poisson) # On choisit le délait d'attente avant de générer un nouveau paquet 
        time.sleep(temps_delta) 
        paquet = Paquet(source=self.getNuméro()) # On génère un paquet 
        print(f"paquet n°{paquet} provenant de {self.getNuméro()} -- temps d'attente : {temps_delta}") 
        self.Insertion(paquet) # On insère le paquet directement dans le Buffer rataché à la source 

    def AfficheTest(self):
        """ Cette fonction est temporaire elle ne sert qu'à afficher l'évolution de la Source pour faciliter les tests sur la classe """
        print(f"Buffer Source {self.getNuméro()} : {self.getListe_attente()}")

    @classmethod
    def Réinitialiser(cls):
        super().Réinitialiser()
        Source.nombre_sources = 0
        Source.liste_sources = []

class Stratégie:
    # Cette classe à pour but d'encapsuler les stratégies de gestion de flux de données

    def Update(self,Buffer_Principal,file_attente,indice_max):
        liste_threads = []    # On initialise la liste des threads qui vont être éxécutés durant la boucle

        liste_threads.append(threading.Thread(target=Buffer_Principal.Transmission(), args=(1,5)))
        liste_threads[0].start() # On démarre la transmission du Buffer Principal 

        for source_ in Source.liste_sources : 
            liste_threads.append(threading.Thread(target=source_.Generateur_paquet(), args=(self.parametre_poisson,)))  # On génère de nouveaux paquets pour chaque source         

        for thread in liste_threads[1:]:
            thread.start()

        for thread in liste_threads[1:]:
            thread.join()

        if self.numéro == 1:
            source_Transmission = None # On initialise la source dont on va transmettre un paquet à None
            capacite_max = 0 # On initialise la capacité locale de la source transmission à 0
            for source_ in Source.liste_sources :
                if source_.getCapacite_locale() > capacite_max:  # On choisit ici la source_ dont la capacite locale est maximale 
                    capacite_max = source_.getCapacite_locale()
                    source_Transmission = source_
        elif self.numéro == 2:
            source_Transmission = file_attente.pop(0) # On retire le premier élément de la file d'attente des sources
            file_attente.append(source_Transmission)  # On lance le thread de tranmsission de la source choisit en amont vers le Buffer principal
        else :
            source_Transmission = file_attente[random.randint(0,indice_max)]  # On prend aléatoirement une source dans la file d'attente

        liste_threads.append(threading.Thread(target=source_Transmission.Transmission()))  # On lance le thread de tranmsission de la source choisit en amont vers le Buffer principal
        liste_threads[-1].start()
        liste_threads[-1].join()

        liste_threads[0].join() # Destination.Transmission()

        if self.Destination.getListe_attente() != []:
            self.Destination.getListe_attente()[-1].setTemps_arrivé(time.time()) # Dès qu'un paquet arrive on stock son temps d'arrivé

    def __init__(self,numéro,nombre_source=2,échantillon=20,parametre_poisson=0.5):
        assert numéro in [1,2,3], "Il n'existe que 3 stratégie différente qui sont : [1,2,3]."
        assert isinstance(nombre_source,int), "Le nombre de sources utilisées dans la simulation doit être un entier."
        # On réinitialise les instances des classes
        Paquet.Réinitialiser()
        Buffer.Réinitialiser()
        Source.Réinitialiser()
        
        Destination = Buffer() 
        Destination.setCapacite_locale(ajout=Buffer.Capacité - échantillon)  # On initialise la capacité local du Buffer Destination pour décider de la taille de l'échantillon de paquets sur lequel nous allons baser nos analyses
        self.numéro = numéro
        self.parametre_poisson = parametre_poisson
        self.Destination = Destination
        DEBUT_TEMPS_TEST = time.time()

        # Initialisation des objets
        Buffer_Principal = Buffer(Destination) # On initialise le Buffer principal 
        for s in range(nombre_source):   # A chaque itération on crée un objet source, qui sera directement stocké dans 'Source.liste_sources' lors de l'initialisation de ceux-ci
            Source(Buffer_Principal)
        Buffer_Principal.setPredecesseur(Source.liste_sources) 

        file_attente = Source.liste_sources  # On initialise une file d'attente qui sera utilisée pour faire alterner le choix de la source par le Buffer principal
        indice_max = len(file_attente)-1 # On initialise l'indice max pouvant être tiré au hasard pour accéder à la file d'attente
        
        while Destination.getCapacite_locale() < Buffer.Capacité:
            self.Update(Buffer_Principal,file_attente,indice_max)

        # Affichages de contôle pour s'assurer du bon fonctionnement du script 
        print(f"Buffer Principal : {Buffer_Principal.getListe_attente()}")
        print(f"Buffer Destination : {Destination.getListe_attente()}") 
        for source_ in Source.liste_sources : 
            source_.AfficheTest()
        self.temps_total = time.time() - DEBUT_TEMPS_TEST
        print(f"\nFin du test !\nLe test a duré : {self.temps_total}")

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



class Interface(customtkinter.CTk):             ### Classe qui gère tout l'aspect visuel du code
    def __init__(self):
        super().__init__()

        ### On définit les caractéristiques de bases
        self.title("Projet 2024 : Stratégies de gestion de flux.py")
        largeur = 680
        longueur = 1400
        self.geometry(f"{longueur}x{largeur}")


        ### On s'occupe ici des éléments de la page d'acceuil
        self.frame_accueil = customtkinter.CTkFrame(self, width=longueur, height= largeur)
        self.frame_accueil.pack_propagate(False)   
        self.frame_accueil.pack()

        self.label_commencer = customtkinter.CTkLabel(self.frame_accueil,font=("Helvetica", 40), 
                                                    text=" Projet 2024 : \n Stratégies de gestion de flux à l’entrée d’un un réseau decommunication.\n\n DESFONTAINES - DESMARES",
                                                    anchor="center")
        self.label_commencer.pack(pady = 120)

        self.bouton_accueil = customtkinter.CTkButton(self.frame_accueil, corner_radius= 40, text= "Commencer !",anchor="center",
                                                       command= self.next_accueil, font=("Arial", 27), height= 30)
        self.bouton_accueil.pack()


        #### Eléments présents sur la page intermerdiaire
        self.strat = customtkinter.CTkEntry(self.frame_accueil, placeholder_text="Entrer un numéro de stratégie")
        self.bouton_demo = customtkinter.CTkButton(self.frame_accueil, text= "Lancer la démonstration ", command= self.next_explications, height= 30, width= 150,
                                                    corner_radius= 30, font= ("Arial", 20))
        self.erreur = customtkinter.CTkLabel(self.frame_accueil, text = "Saisie invalide. Ré-essayez !", font = ("Arial", 40), text_color="red")
        self.bouton_analyses = customtkinter.CTkButton(self.frame_accueil, text= "Comparer les 3 stratégies", command= self.next_analyses,font= ("Arial", 20),
                                                       corner_radius= 30, height= 30, width= 150)



        ### On s'occupe de la page où la démonstration se fait
        self.frame_principal = customtkinter.CTkFrame(self, width=1000, height=400)
        self.frame_principal.pack_forget()
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(1, weight=1)


        ### On s'occupe des composants de la page d'analyses
        self.frame_analyses = customtkinter.CTkFrame(self, width= longueur, height= largeur)
        self.frame_analyses.grid_propagate(False)
        
        self.frame_test1 = customtkinter.CTkFrame(self.frame_analyses, width = 400, height= 500)
        self.frame_test2 = customtkinter.CTkFrame(self.frame_analyses, width = 400, height= 500)
        self.frame_test3 = customtkinter.CTkFrame(self.frame_analyses, width = 400, height= 500)
        self.frame_test1.grid_propagate(False)
        self.frame_test2.grid_propagate(False)
        self.frame_test3.grid_propagate(False)

        self.label_test1 = customtkinter.CTkLabel(self.frame_test1, text="", bg_color= "transparent", anchor = "center")
        self.label_test2 = customtkinter.CTkLabel(self.frame_test2, text="", bg_color= "transparent", anchor = "center")
        self.label_test3 = customtkinter.CTkLabel(self.frame_test3, text="", bg_color= "transparent", anchor = "center")

        self.bouton_quitter = customtkinter.CTkButton(self.frame_analyses, text= "Quitter", command= self.quit_app, font= ("Arial", 20),
                                                       corner_radius= 30, height= 30, width= 150 )
        



        ### On créée des boites pour chacun des buffers et pouvoir illustrer l'ajout, le retrait et la transmission d'un paquet
        mes_buffers = []
        buffer = Buffer.liste_buffers[::-1]
        for k in range(4): ### 4 car on fait nos tests avec deux buffers sources +  un buffer principal + un buffer destination
            ### On créée les "boites" à tour de rôle et on les positionnes de différentes manières, selon le buffer auquel correspond la "boite"
            self.frame_source = customtkinter.CTkFrame(self.frame_principal,width=100, height= 300, corner_radius=10, fg_color= "black")

            if k == 0 :
                self.frame_source.grid(column = 0, row = 0, pady = 10, padx = 10, sticky = "nsew")
                self.frame_principal.grid_columnconfigure(0, weight=1, uniform="buffers")
                self.frame_principal.grid_rowconfigure(0, weight=1, uniform="buffers")
            elif k == 1:
                self.frame_source.grid(column = 0, row = 1, pady = 10, padx = 10, sticky = "nsew")
                self.frame_principal.grid_columnconfigure(0, weight=1, uniform="buffers")
                self.frame_principal.grid_rowconfigure(1, weight=1, uniform="buffers")
            elif k == 2:
                self.frame_source.grid(column = 1, row = 0, rowspan = 2, pady = 10, padx = 10, sticky = "nsew")
                self.frame_principal.grid_columnconfigure(1, weight=1, uniform="buffers")
                self.frame_principal.grid_rowconfigure(0, weight=1, uniform="buffers")
                self.frame_principal.grid_rowconfigure(1, weight=1, uniform="buffers")
            else : 
                self.frame_source.grid(column = 2,row = 0, rowspan = 2, pady = 10, padx = 10, sticky = "nsew")
                self.frame_principal.grid_columnconfigure(2, weight=1, uniform="buffers")
                self.frame_principal.grid_rowconfigure(0, weight=1, uniform="buffers")
                self.frame_principal.grid_rowconfigure(1, weight=1, uniform="buffers")
            mes_buffers.append(self.frame_source)

        
    ###   Méthode qui récupère que le chiffre saisi par l'utilisateur, et lance en conséquence la démonstration correspondante
    def next_explications(self):
        if  not isinstance(self.strat,int):
            self.erreur.place( x = 440, y = 530)
        strategie = int(self.strat.get())
        if strategie not in [1,2,3]:
            self.erreur.place( x = 440, y = 530)
        else:
            self.frame_accueil.destroy()
            self.frame_principal.pack_propagate(False)
            self.frame_principal.pack(pady = 20, fill = "both", expand = True)
            if strategie == 1: 
                self.demo_strat1()
            elif strategie == 2 :
                self.demo_start2()
            else :
                self.demo_strat3()


    def next_accueil(self):   ### Méthode qui permet d'afficher la page précédent la page d'accueil, la page où l'on demande à l'utilisateur quelle stratégie adopter.
        self.label_commencer.configure(text = "Il vous est demandé ici de choisir une stratégie à adopter pour la démonstration.\n"
                                       " Vous avez 3 stratégies de gestion de la file d'attente possibles : \n"
                                       "   – La file d’attente choisie est celle contenant le plus grand nombre de paquets.\n"
                                       "   – Un paquet est pris de chaque file d’attente, à tour de rôle.\n"
                                       "   – La file d’attente est choisie de manière aléatoire.\n"
                                       "Entrez 1, 2 ou 3 puis appuyez sur le bouton.", font=("Helvetica", 30))
        self.bouton_accueil.destroy()
        self.strat.place(x = 630, y = 380)
        self.bouton_demo.pack()
        self.bouton_analyses.place(x = 570, y = 500)


    ###   Méthode qui permet de lancer 3 tests avec des stratégies différentes, récupérer les données et les afficher afin de permettre une comparaison
    def recup_data(self): 
        liste_data = []

        ###   On lance 3 stratégies différentes, sur un même nombre d'échantillon pour pouvoir les comparer par la suite
        Strat1 = Stratégie(1,2,1,0.5)
        Strat2 = Stratégie(2,2,1,0.5)
        Strat3 = Stratégie(3,2,1,0.5)

        ###   On stocke ici les données d'analyses obtenues, à la liste liste_data
        liste_data.append((Strat1.Analyse_Temps(), Strat1.Analyse_Taux(), Strat1.temps_total))
        liste_data.append((Strat2.Analyse_Temps(), Strat2.Analyse_Taux(), Strat2.temps_total))
        liste_data.append((Strat3.Analyse_Temps(), Strat3.Analyse_Taux(), Strat3.temps_total))

        ###   On affiche les données
        self.label_test1.configure(text = f"Résultats Strat 1 \n\n\n\n temps moyen d'attente : {round(liste_data[0][0], 2)} s \n\n "
                                   f"taux de perte : {round(liste_data[0][1],2)} \n\n durée du test :{round(liste_data[0][2],2)} s", font = ("Arial", 20))
        self.label_test2.configure(text = f"Résultats Strat 2 \n\n\n\n temps moyen d'attente : {round(liste_data[1][0], 2)} s \n\n "
                                   f"taux de perte : {round(liste_data[1][1],2)} \n\n durée du test :{round(liste_data[1][2],2)} s", font = ("Arial", 20))
        self.label_test3.configure(text = f"Résultats Strat 3 \n\n\n\n temps moyen d'attente : {round(liste_data[2][0], 2)} s \n\n "
                                   f"taux de perte : {round(liste_data[2][1],2)} \n\n durée du test :{round(liste_data[2][2],2)} s", font = ("Arial", 20))

        self.label_test1.grid(padx = 55, pady = 150)
        self.label_test2.grid(padx = 55, pady = 150)
        self.label_test3.grid(padx = 55, pady = 150)


    def next_analyses(self):   ### Méthode qui permet de changer de page, et d'afficher celle qui présente les résultats d'analyses
        self.frame_accueil.destroy()
        self.frame_analyses.grid()     
        self.frame_test1.grid(column = 0, row = 0, padx = 40, pady = 20)
        self.frame_test2.grid(column = 1, row = 0, padx = 20, pady = 20)
        self.frame_test3.grid(column = 2, row = 0, padx = 40, pady = 20)
        self.bouton_quitter.grid(column = 1, row = 1, pady = 20)
        self.recup_data()

    def quit_app(self):    ###   Méthode qui détruit complétement la fenetre d'interface graphique.
        self.destroy()


    def same_place(self, paquet_a_deplacer, my_x, x_destination): ###   Méthode qui permet juste de faire une pause dans l'animation du paquet_a_deplacer
            app.after(300, lambda : self.deplacer(paquet_a_deplacer, my_x, x_destination))   ### Cette ligne permet de relancer le déplacement du paquet_a_deplacer


    ###   Méthode qui change la coordonnée x du paquet_a_deplacer, et le ré-affiche en fonction de sa nouvelle position. 
    def deplacer(self, paquet_a_deplacer, my_x, x_destination):
            my_x += 40
            if my_x < 740:    ###   Cela correspond au moment où le paquet se trouve entre sa position initiale et sa position intermediaire (dans le buffer principal)
                paquet_a_deplacer.place(x = my_x)
                app.after(300, lambda : self.deplacer(paquet_a_deplacer, my_x, x_destination))
            elif my_x == 740:   ###   Cela correspond au moment où le paquet se trouve à sa position intermediaire (dans le buffer principal)
                app.after(200, lambda : self.same_place(paquet_a_deplacer, my_x, x_destination))
            elif 741 < my_x < x_destination:   ###  Cela correspond au moment où le paquet se trouve entre sa position intermediaire et sa position finale (dans le buffer Destination)
                paquet_a_deplacer.place(x = my_x)
                app.after(300, lambda : self.deplacer(paquet_a_deplacer, my_x, x_destination))


    ###   Méthode qui lance l'animation de la stratégie 1
    def demo_strat1(self):
        paquet1_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet1_source1.place(x = 200, y = 100)

        paquet2_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet2_source1.place(x = 150, y = 100)

        paquet3_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet3_source1.place(x =100, y = 100)

        paquet4_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet4_source1.place(x = 150, y = 150)

        paquet5_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet5_source1.place(x = 100, y = 150)

        paquet1_source2 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="red", text = "")
        paquet1_source2.place(x = 150, y = 400)

        paquet2_source2 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="red", text = "")
        paquet2_source2.place(x = 100, y = 400)

        self.deplacer(paquet1_source1, 200, 1300)
        app.after(3500,lambda : self.deplacer(paquet2_source1, 150, 1250))
        app.after(7000,lambda : self.deplacer(paquet3_source1, 100, 1200))
        app.after(10500,lambda : self.deplacer(paquet4_source1, 150, 1250))
        app.after(14000,lambda : self.deplacer(paquet1_source2, 150, 1250))
        app.after(17500,lambda : self.deplacer(paquet5_source1, 100, 1200))
        app.after(21000,lambda : self.deplacer(paquet2_source2, 100, 1200))


    ###   Méthode qui lance l'animation de la stratégie 2
    def demo_start2(self):
        paquet1_source1 = customtkinter.CTkLabel(self.frame_principal, width= 30, height= 30, bg_color="blue", text = "")
        paquet1_source1.place(x = 200, y = 100)

        paquet2_source1 = customtkinter.CTkLabel(self.frame_principal, width= 30, height= 30, bg_color="blue", text = "")
        paquet2_source1.place(x = 150, y = 100)

        paquet3_source1 = customtkinter.CTkLabel(self.frame_principal, width= 30, height= 30, bg_color="blue", text = "")
        paquet3_source1.place(x =100, y = 100)

        paquet1_source2 = customtkinter.CTkLabel(self.frame_principal, width= 30, height= 30, bg_color="red", text = "")
        paquet1_source2.place(x = 200, y = 400)

        paquet2_source2 = customtkinter.CTkLabel(self.frame_principal, width= 30, height= 30, bg_color="red", text = "")
        paquet2_source2.place(x = 150, y = 400)

        self.deplacer(paquet1_source1, 200, 1300)
        app.after(3500,lambda : self.deplacer(paquet1_source2, 200, 1300))
        app.after(7000,lambda : self.deplacer(paquet2_source1, 150, 1250))
        app.after(10500,lambda : self.deplacer(paquet2_source2, 150, 1250))
        app.after(14000,lambda : self.deplacer(paquet3_source1, 100, 1200))


    ###   Méthode qui lance l'animation de la stratégie 3
    def demo_strat3(self):
        paquet1_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet1_source1.place(x = 200, y = 100)

        paquet2_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet2_source1.place(x = 150, y = 100)

        paquet3_source1 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="blue", text = "")
        paquet3_source1.place(x =100, y = 100)

        paquet1_source2 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="red", text = "")
        paquet1_source2.place(x = 200, y = 400)

        paquet2_source2 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="red", text = "")
        paquet2_source2.place(x = 150, y = 400)

        paquet3_source2 = customtkinter.CTkLabel(app, width= 30, height= 30, bg_color="red", text = "")
        paquet3_source2.place(x = 100, y = 400)


        self.deplacer(paquet1_source2, 200, 1300)
        app.after(3500,lambda : self.deplacer(paquet2_source2, 150, 1250))
        app.after(7000,lambda : self.deplacer(paquet1_source1, 200, 1300))
        app.after(10500,lambda : self.deplacer(paquet3_source2, 100, 1200))
        app.after(14000,lambda : self.deplacer(paquet2_source1, 150, 1250))
        app.after(17500,lambda : self.deplacer(paquet3_source1, 100, 1200))
        

if __name__ == "__main__":
    app = Interface()
    app.mainloop()