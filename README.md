# MQTT App with Tkinter

## Description

Ce projet implémente une application graphique MQTT (Message Queuing Telemetry Transport) en Python avec `Tkinter`, permettant à l'utilisateur de se connecter à un serveur MQTT, envoyer des messages dans différents formats (texte, JSON, Base64, Hex), et effectuer des actions spécifiques comme déplacer un robot, le faire pivoter, ou envoyer des commandes personnalisées. Il est compatible avec les langues française et anglaise, configurables depuis une fenêtre de sélection au lancement de l'application.

## Fonctionnalités

- Connexion à un serveur MQTT avec un support d'authentification (nom d'utilisateur et mot de passe).
- Interface utilisateur graphique conviviale en Tkinter avec un design moderne.
- Envoi de messages sur un topic MQTT en plusieurs formats : texte brut, JSON, Base64, et Hex.
- Support de plusieurs actions robotiques : `Move`, `Rotate`, `Pickup`, `Position`, `Putback`, et `Stop`.
- Sélection de la langue de l'application (anglais ou français).
- Affichage des logs des messages envoyés et reçus.
- Fenêtre de confirmation avant l'envoi des messages et des actions.

## Prérequis

Assurez-vous d'avoir Python installé, de préférence une version 3.7 ou ultérieure.

### Bibliothèques nécessaires

Le projet utilise les bibliothèques suivantes :

- `Tkinter` pour l'interface graphique (inclus par défaut avec Python).
- `paho-mqtt` pour la connexion MQTT.
- `json`, `base64`, et `binascii` pour les traitements de message.

Installez `paho-mqtt` en utilisant pip :

```bash
pip install paho-mqtt
```

## Structure de l'interface utilisateur

- **Configuration de connexion** : Champ pour l'adresse IP du broker MQTT, le port, le topic, le nom d'utilisateur et le mot de passe.
- **Zone de log** : Affiche les logs des actions et messages.
- **Message** : Champ pour entrer le message et son type (`Text`, `JSON`, `BASE64`, `Hex`, `CBOR`).
- **Boutons** :
  - **Connect** : Se connecte au broker MQTT.
  - **Send Message** : Envoie le message vers le broker.
  - **Robot Action** : Ouvre une fenêtre pour envoyer des commandes au robot.
  - **Stop Robot** : Envoie une commande pour arrêter le robot.

## Fonctionnement du code

1. **Sélection de la langue**  
   Lors du lancement, une fenêtre demande à l'utilisateur de sélectionner une langue (anglais ou français). Une fois choisie, l'application principale se lance avec l'interface dans la langue sélectionnée.

2. **Connexion au broker MQTT**  
   L'utilisateur entre les informations du broker MQTT et clique sur le bouton **Connect**. Le programme tente ensuite de se connecter et affiche un message de réussite ou d'échec dans la zone de log.

3. **Envoi de messages**  
   L'application permet d'envoyer un message dans un format sélectionné (`Text`, `JSON`, `BASE64`, `Hex`). Le message est envoyé sur le topic spécifié par l'utilisateur. Le programme demande une confirmation avant l'envoi du message.

4. **Actions du robot**  
   L'application propose plusieurs actions robotisées :
   - **Move** : Le robot peut se déplacer dans une direction (gauche/droite) sur une distance en centimètres.
   - **Rotate** : Le robot peut pivoter à un angle donné.
   - **Pickup**, **Position**, **Putback** : Envoi de commandes pour ramasser, placer ou repositionner un objet.
   - **Stop** : Commande pour arrêter le robot.

## Améliorations possibles

- **Ajout de nouveaux types d'action et personnalisation du robot.**
- **Support pour des brokers sécurisés avec TLS.**
- **Intégration de nouvelles langues.**
- **Sauvegarde et chargement des préférences utilisateur (dernier broker utilisé, topic favori, etc.).**
