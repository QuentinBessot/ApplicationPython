import tkinter as tk
from tkinter import messagebox  # Importer messagebox pour la popup
import speech_recognition as sr
import threading
import paho.mqtt.client as mqtt
import json  # Importer le module JSON pour construire le message

# Initialiser le client MQTT
client = mqtt.Client()

# Fonction pour se connecter au broker MQTT
def connecter_mqtt():
    broker_address = broker_entry.get()
    broker_port = int(port_entry.get())
    mqtt_topic = topic_entry.get()

    try:
        client.connect(broker_address, broker_port)
        connection_status.config(text="Connecté au broker MQTT", fg="green")
        global MQTT_TOPIC
        MQTT_TOPIC = mqtt_topic
    except Exception as e:
        connection_status.config(text=f"Échec de la connexion : {e}", fg="red")

# Fonction pour afficher la popup si un mot spécifique est détecté
def afficher_popup(message):
    messagebox.showinfo("Mot détecté", f"Le mot '{message}' a été détecté !")

# Liste de mots spécifiques à détecter
mots_specifiques = ["move", "stop", "hello"]

# Fonction de reconnaissance vocale
def ecouter_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Parlez maintenant...", bg="#F8D7DA", fg="#721C24")
        root.update_idletasks()
        print("Parlez maintenant...")  # Affiche dans la console

        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=5)
            texte = recognizer.recognize_google(audio, language="en-US")
            print("Vous avez dit :", texte)
            result_label.config(text=f"Vous avez dit : {texte}", fg="#155724", bg="#D4EDDA")
            client.publish(MQTT_TOPIC, texte)

            # Vérifier si un des mots spécifiques est détecté dans le texte
            for mot in mots_specifiques:
                if mot in texte.lower():
                    afficher_popup(mot)  # Affiche une popup pour chaque mot détecté
                    # Si le mot "hello" est détecté, envoyer un message JSON
                    if mot == "hello":
                        message_json = json.dumps({"name": "hello"})
                        client.publish(MQTT_TOPIC, message_json)
                        print("Message JSON envoyé :", message_json)

                    if mot == "move":
                        message_json = json.dumps({"name": "Move"})
                        client.publish(MQTT_TOPIC, message_json)
                        print("Message JSON envoyé :", message_json)

        except sr.UnknownValueError:
            error_message = "Je n'ai pas compris ce que vous avez dit."
            print(error_message)
            result_label.config(text=error_message, fg="#721C24", bg="#F8D7DA")
            client.publish(MQTT_TOPIC, error_message)
        except sr.RequestError:
            error_message = "Erreur de connexion à l'API."
            print(error_message)
            result_label.config(text=error_message, fg="#721C24", bg="#F8D7DA")
            client.publish(MQTT_TOPIC, error_message)
        except sr.WaitTimeoutError:
            error_message = "Temps d'attente dépassé. Veuillez réessayer."
            print(error_message)
            result_label.config(text=error_message, fg="#721C24", bg="#F8D7DA")
            client.publish(MQTT_TOPIC, error_message)

        # Mettre à jour l'interface pour signaler la fin de l'enregistrement
        status_label.config(text="Enregistrement fini", bg="#D4EDDA", fg="#155724")
        root.update_idletasks()

# Fonction pour démarrer la reconnaissance vocale dans un nouveau thread
def lancer_reconnaissance():
    thread = threading.Thread(target=ecouter_microphone)
    thread.start()

# Créer la fenêtre principale
root = tk.Tk()
root.title("Reconnaissance Vocale avec MQTT")

# Dimensions de la fenêtre
root.geometry("400x450")
root.config(bg="#E9ECEF")

# Ajouter les champs d'entrée pour la connexion MQTT
tk.Label(root, text="Adresse du broker :", bg="#E9ECEF").pack(pady=5)
broker_entry = tk.Entry(root, font=("Helvetica", 12))
broker_entry.pack(pady=5)

tk.Label(root, text="Port du broker :", bg="#E9ECEF").pack(pady=5)
port_entry = tk.Entry(root, font=("Helvetica", 12))
port_entry.insert(0, "1883")
port_entry.pack(pady=5)

tk.Label(root, text="Sujet MQTT :", bg="#E9ECEF").pack(pady=5)
topic_entry = tk.Entry(root, font=("Helvetica", 12))
topic_entry.pack(pady=5)

# Bouton pour établir la connexion MQTT
connect_button = tk.Button(root, text="Connecter MQTT", font=("Helvetica", 12), command=connecter_mqtt, bg="#28A745",
                           fg="white")
connect_button.pack(pady=10)

# Label pour afficher l'état de la connexion MQTT
connection_status = tk.Label(root, text="Non connecté", font=("Helvetica", 10), fg="red", bg="#E9ECEF")
connection_status.pack(pady=5)

# Ajouter un label de statut avec un fond coloré
status_label = tk.Label(root, text="Cliquez sur 'Démarrer' pour parler", font=("Helvetica", 14), bg="#D1ECF1",
                        fg="#0C5460", relief="solid", padx=10, pady=10)
status_label.pack(pady=20)

# Ajouter un bouton pour démarrer la reconnaissance vocale
start_button = tk.Button(root, text="Démarrer", font=("Helvetica", 14), command=lancer_reconnaissance, bg="#007BFF",
                         fg="white", relief="flat", height=2, width=15)
start_button.pack(pady=10)

# Ajouter un label pour afficher le texte reconnu
result_label = tk.Label(root, text="", font=("Helvetica", 12), wraplength=300, bg="#FFFFFF", fg="#333333",
                        relief="sunken", padx=10, pady=10)
result_label.pack(pady=20)

# Démarrer l'interface graphique
root.mainloop()
