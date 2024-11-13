import tkinter as tk
import paho.mqtt.client as mqtt
import json  # Importation de la bibliothèque json

class MQTTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application MQTT")

        # Configurer la taille initiale de la fenêtre
        self.root.geometry("800x600")

        # Configure les lignes et les colonnes pour qu'elles puissent se redimensionner
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1, minsize=30)  # Lignes redimensionnables
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1, minsize=100)  # Colonnes redimensionnables

        # Labels et champs de texte
        self.broker_label = tk.Label(root, text="Adresse du Broker MQTT:")
        self.broker_label.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.broker_ip = tk.Entry(root)
        self.broker_ip.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        self.port_label = tk.Label(root, text="Port (par défaut 1883):")
        self.port_label.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.broker_port = tk.Entry(root)
        self.broker_port.insert(tk.END, "1883")
        self.broker_port.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        self.topic_label = tk.Label(root, text="Topic:")
        self.topic_label.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.topic = tk.Entry(root)
        self.topic.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)

        # Champs pour nom d'utilisateur et mot de passe
        self.username_label = tk.Label(root, text="Nom d'utilisateur:")
        self.username_label.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=3, column=1, sticky='nsew', padx=10, pady=10)

        self.password_label = tk.Label(root, text="Mot de passe:")
        self.password_label.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
        self.password_entry = tk.Entry(root, show="*")  # Le mot de passe est masqué
        self.password_entry.grid(row=4, column=1, sticky='nsew', padx=10, pady=10)

        # Zone de message pour afficher les logs
        self.msg_box = tk.Text(root, height=10, width=40, state='disabled')
        self.msg_box.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Champ pour saisir un message à envoyer
        self.message_label = tk.Label(root, text="Message à envoyer (en JSON):")
        self.message_label.grid(row=6, column=0, sticky='nsew', padx=10, pady=10)
        self.message_entry = tk.Entry(root)
        self.message_entry.grid(row=6, column=1, sticky='nsew', padx=10, pady=10)

        # Bouton pour se connecter au broker
        self.connect_button = tk.Button(root, text="Se connecter", command=self.connect_to_broker)
        self.connect_button.grid(row=7, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Bouton pour envoyer un message
        self.send_button = tk.Button(root, text="Envoyer Message", command=self.send_message)
        self.send_button.grid(row=8, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Création du client MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect_to_broker(self):
        broker_ip = self.broker_ip.get()
        broker_port = int(self.broker_port.get())
        topic = self.topic.get()

        # Récupérer le nom d'utilisateur et le mot de passe
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Si un nom d'utilisateur et un mot de passe sont fournis, les ajouter à la connexion
        if username and password:
            self.client.username_pw_set(username, password)

        self.client.user_data_set({'topic': topic})
        self.client.connect(broker_ip, broker_port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.log_message("Connexion réussie au broker MQTT!")
            client.subscribe(userdata['topic'])
        else:
            self.log_message("Échec de connexion, code de retour: " + str(rc))

    def on_message(self, client, userdata, msg):
        self.log_message(f"Message reçu sur {msg.topic}: {msg.payload.decode()}")

    def send_message(self):
        # Récupérer le message à envoyer
        message = self.message_entry.get()
        topic = self.topic.get()

        if message and topic:
            try:
                # Essayer de convertir le message en JSON
                json_message = json.loads(message)  # Vérifier si le message est un JSON valide
                self.client.publish(topic, json.dumps(json_message))  # Convertir en JSON et envoyer
                self.log_message(f"Message envoyé sur {topic}: {json.dumps(json_message)}")
            except json.JSONDecodeError:
                self.log_message("Erreur: Le message n'est pas un JSON valide.")
        else:
            self.log_message("Erreur: Il faut saisir un message et un topic.")

    def log_message(self, message):
        self.msg_box.config(state='normal')
        self.msg_box.insert(tk.END, message + '\n')
        self.msg_box.yview(tk.END)
        self.msg_box.config(state='disabled')


# Créer l'interface Tkinter
root = tk.Tk()
app = MQTTApp(root)
root.mainloop()
