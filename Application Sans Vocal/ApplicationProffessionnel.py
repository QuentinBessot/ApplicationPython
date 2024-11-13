import tkinter as tk
from tkinter import ttk, messagebox
import paho.mqtt.client as mqtt
import json
import base64
import binascii


class MQTTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application MQTT")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f2f5")

        self.root.option_add("*Font", "Helvetica 12")

        # Cadre pour la configuration de connexion
        self.config_frame = tk.Frame(root, bg="#e9ecef", padx=10, pady=10, relief="ridge", bd=2)
        self.config_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Champs de texte et labels pour le broker
        self.add_label_and_entry(self.config_frame, "Adresse du Broker MQTT:", 0, "broker_ip")
        self.add_label_and_entry(self.config_frame, "Port (par défaut 1883):", 1, "broker_port", default="1883")
        self.add_label_and_entry(self.config_frame, "Topic:", 2, "topic")
        self.add_label_and_entry(self.config_frame, "Nom d'utilisateur:", 3, "username")
        self.add_label_and_entry(self.config_frame, "Mot de passe:", 4, "password", show="*")

        # Zone de log
        self.log_frame = tk.LabelFrame(root, text="Logs", bg="#f0f2f5", font="Helvetica 12 bold", padx=10, pady=10)
        self.log_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        self.msg_box = tk.Text(self.log_frame, height=10, width=50, state='disabled', bg="#ffffff", fg="#333333")
        self.msg_box.pack(expand=True, fill="both")

        # Champ de message à envoyer
        self.message_label = tk.Label(root, text="Message à envoyer:", bg="#f0f2f5", font="Helvetica 12 bold")
        self.message_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # Zone de texte pour saisir un message plus grand
        self.message_entry = tk.Text(root, height=5, font="Helvetica 12")  # Augmenter la hauteur pour plus d’espace
        self.message_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

        # Menu déroulant pour le type de message
        self.message_type_label = tk.Label(root, text="Type de message:", bg="#f0f2f5", font="Helvetica 12 bold")
        self.message_type_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.message_type = ttk.Combobox(root, values=["Text", "JSON", "BASE64", "Hex"], state="readonly")
        self.message_type.current(0)  # Définir la valeur par défaut sur "Text"
        self.message_type.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

        # Boutons
        self.connect_button = tk.Button(root, text="Se connecter", command=self.connect_to_broker, bg="#007bff",
                                        fg="white", font="Helvetica 12 bold", relief="groove")
        self.connect_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.send_button = tk.Button(root, text="Envoyer Message", command=self.send_message, bg="#28a745", fg="white",
                                     font="Helvetica 12 bold", relief="groove")
        self.send_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Configuration du client MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def add_label_and_entry(self, parent, label_text, row, entry_name, default="", show=None):
        label = tk.Label(parent, text=label_text, bg="#e9ecef", font="Helvetica 12 bold")
        label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(parent, font="Helvetica 12", show=show)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        if default:
            entry.insert(tk.END, default)
        setattr(self, entry_name, entry)

    def connect_to_broker(self):
        broker_ip = self.broker_ip.get()
        broker_port = int(self.broker_port.get())
        topic = self.topic.get()
        username = self.username.get()
        password = self.password.get()

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
        message = self.message_entry.get("1.0", tk.END).strip()
        topic = self.topic.get()
        message_type = self.message_type.get()

        if message and topic:
            try:
                if message_type == "JSON":
                    json_message = json.loads(message)
                    payload = json.dumps(json_message)
                elif message_type == "BASE64":
                    payload = base64.b64encode(message.encode()).decode()
                elif message_type == "Hex":
                    payload = binascii.hexlify(message.encode()).decode()
                else:
                    payload = message  # Par défaut, le type "Text" envoie le message tel quel

                self.client.publish(topic, payload)
                self.log_message(f"Message envoyé sur {topic} [{message_type}]: {payload}")
            except (json.JSONDecodeError, binascii.Error) as e:
                self.log_message(f"Erreur: Impossible d'envoyer le message ({e})")
                messagebox.showerror("Erreur", f"Format du message incorrect pour {message_type}")
        else:
            self.log_message("Erreur: Il faut saisir un message et un topic.")

    def log_message(self, message):
        self.msg_box.config(state='normal')
        self.msg_box.insert(tk.END, message + '\n')
        self.msg_box.yview(tk.END)
        self.msg_box.config(state='disabled')


# Création de l'interface Tkinter
root = tk.Tk()
app = MQTTApp(root)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)  # Pour la zone de log
root.mainloop()
