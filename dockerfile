# Utiliser une image de base avec Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirements.txt /app/requirements.txt

# Installer les dépendances à partir du fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet dans le conteneur
COPY . /app

# Exposer le port si nécessaire (remplace 8000 par ton port si l'appli utilise un port spécifique)
EXPOSE 8000

# Commande pour exécuter ton script main.py
CMD ["python", "main.py"]
