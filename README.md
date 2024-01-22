# Drone_project


AUTOMATIK DRONE
4/10/2023
─
LE BERRE Adrien
CORNUT Oscar
EL MOUSSAHOUI Suhayl
AZIZAJ Emile
KADDAR Yassine
Lycée Charlemagne 
rue Charlemagne
Vue d'ensemble
Notre projet est un drône industriel qui va pouvoir reconnaître des objets à l’aide d’une IA afin de pouvoir les récupérer pour les ranger. 
Tâches :
machine learning et path finding: Suhayl
trouver des objet à l’aide de la détection d’images
calcul de distance entre drône et objet 
réaliser le path finding

Vol automatique et accrochage: Emile
Le drone doit pouvoir être capable, lorsqu'il connaît sa position et la position de sa destination, de se déplacer seul de manière équilibré
Il doit pouvoir détecter un objet sur son trajet, et s'arrêter de lui-même. Il doit ensuite envoyer une requête de nouveau trajet à son algorithme de pathfinding
Le drone doit être capable lorsqu'il est à la bonne position, de descendre progressivement à la bonne hauteur du sol, s'accrocher à l'aide d'une pince à l'objet, et renvoyer une variable accroche True pour remonter et débuter le trajet vers la boîte de rangement.
Une fois arrivé à la boite, il doit être capable de descendre progressivement et de lâcher délicatement l'objet pour ne pas le casser

Un mode manuel du drône, pouvoir commander le drône à l’aide d’une manette: Adrien
Pouvoir contrôler depuis un opérateur les direction principale du drone, haut, bas, gauche, droite, et pouvoir voir sa caméra (via l’application mobile)
des touches de fonctions : faire un backflip, un 360 degré, atterrir,,rester en l'air sans bouger etc


création d’application: Oscar
différents modes du drône : automatique, suivis et pointing, manuel
avoir un mode manuel sur l’application afin de contrôler le drône via l’application
se connecter au drône avec un mot de passe
Sécuriser la communication entre l’appareil et le drone : Yassine 
Encryption AES-256 bits minimum, SSH, connexion SSH et connexion via vpn via OpenVPN, et création d'un réseau wifi local en wpa3  pour éviter les problèmes d'instabilité 


bibliothèque :
kivy-2.3.0
opencv-python-4.9.0.80
djitellopy-2.5.0
