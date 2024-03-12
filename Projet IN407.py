### Projet IN407

class Paquet:
    nombre_paquets = 0
    def __init__(self,source=0,valeur=1.5):
        Paquet.nombre_paquets += 1
        self.valeur = valeur
        self.source = source

class Source:
    nombre_sources = 0
    def __init__(self):
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
            yield Paquet(source=self.numéro)   #### Pour l'instant les paquets vont dans le vide, est ce qu'il faudrait les stocker dans une liste en locale de l'objet
                                                ### ou directement l'intégrer dans un buffer ou le transmettre ? Cela soulève notamment le problème de "refresh" de la fonction si elle est passé en argument de 'list()'

    def Stop_generateur_paquet(self):
        self.active = False # C'est une première idée certainement maladroite et inadaptée aux threads, il serait sûrement plus simple de mettre fin au thread dans lequel 'Generateur_paquet()' à été lancé
                            # Ou il faudrait que cette fonction soit lancée dans le même ""espace mémoire"" que le thread de la fonction 'Generateur_paquet()' --> ou utiliser la communication entre les processus
        
class Buffer:
    nombre_buffers = 0
    Capacité = 100 
    def __init__(self,predecesseur=None,successeur=None):
        # L'idée derrière prédescesseur et successeur est de lier les buffer entre eux, mais aussi à leur Source notamment pour simplifier la transmission des paquets
        # Remarque : un buffer peut avoir plusieurs prédescesseurs 
        self.predecesseur = predecesseur
        self.successeur = successeur
        liste_attente = []
        self.liste_attente = liste_attente
        capacite_locale = len(liste_attente)
        self.capacite_locale = capacite_locale

        if self.successeur.capacite_locale < Buffer.Capacité:
            instruction_anti_erreur_à_suprimer = True
            # oui ça viendra ! L'idée est ici de déclencher la transmission d'un paquet du buffer vers son successeur

    def Insertion(self,paquet:'Paquet'):
        if self.capacite_locale < Buffer.Capacité:
            self.liste_attente.append(paquet)