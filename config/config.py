# Configuration de la base de données MySQL
DATABASE_CONFIG = {
    "host": "localhost",
    "user": "votre_utilisateur_mysql",
    "password": "votre_mot_de_passe_mysql",
    "database": "votre_base_de_données"
}

# Paramètres de sécurité
SECRET_KEY = "votre_clé_secrète"  # Remplacez par une clé secrète sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Durée de validité des jetons d'accès en minutes

# Autres paramètres de configuration
DEBUG = True  # Active le mode de débogage en développement
