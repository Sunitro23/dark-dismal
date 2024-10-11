# Utiliser une image de base avec Python
FROM python:3.9-slim

# Definir le repertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY ./requirements.txt /app/requirements.txt

# Installer les dependances à partir du fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet dans le conteneur
COPY . /app

# Exposer le port si necessaire (remplace 8000 par ton port si l'appli utilise un port specifique)
EXPOSE 8000

# Commande pour executer ton script main.py
CMD ["python", "main.py"]
