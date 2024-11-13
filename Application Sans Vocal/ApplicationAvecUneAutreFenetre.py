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
        self.message_entry = tk.Text(root, height=2,width=30, font="Helvetica 12")
        self.message_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

        # Menu déroulant pour le type de message
        self.message_type_label = tk.Label(root, text="Type de message:", bg="#f0f2f5", font="Helvetica 12 bold")
        self.message_type_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.message_type = ttk.Combobox(root, values=["Text", "JSON", "BASE64", "Hex", "CBOR"], state="readonly")
        self.message_type.current(0)
        self.message_type.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

        # Boutons
        self.connect_button = tk.Button(root, text="Se connecter", command=self.connect_to_broker, bg="#007bff",
                                        fg="white", font="Helvetica 12 bold", relief="groove")
        self.connect_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.send_button = tk.Button(root, text="Envoyer Message", command=self.send_message, bg="#28a745", fg="white",
                                     font="Helvetica 12 bold", relief="groove")
        self.send_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Bouton pour ouvrir une nouvelle fenêtre
        self.new_window_button = tk.Button(root, text="Action du Robot", command=self.open_new_window,
                                           bg="#6c757d", fg="white", font="Helvetica 12 bold", relief="groove")
        self.new_window_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

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
                    payload = message

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

    def open_new_window(self):
        # Crée une nouvelle fenêtre
        new_window = tk.Toplevel(self.root)
        new_window.title("Actions - MQTT")
        new_window.geometry("400x350")

        # Label pour le choix de l'action
        tk.Label(new_window, text="Choisissez une action :", font="Helvetica 12 bold").pack(pady=10)

        # Menu déroulant pour les actions MOVE et ROTATE
        self.action_choice = ttk.Combobox(new_window, values=["Move", "Rotate","Pickup","Place","Putback","Position"], state="readonly", font="Helvetica 12")
        self.action_choice.current(0)  # Sélectionne MOVE par défaut
        self.action_choice.pack(pady=10)

        # Champs pour la direction, la distance et l'angle
        self.direction_label = tk.Label(new_window, text="Direction (gauche/droite):", font="Helvetica 12")
        self.direction_label.pack(pady=5)
        self.direction_entry = tk.Entry(new_window, font="Helvetica 12")
        self.direction_entry.pack(pady=5)

        self.distance_label = tk.Label(new_window, text="Distance en cm:", font="Helvetica 12")
        self.distance_label.pack(pady=5)
        self.distance_entry = tk.Entry(new_window, font="Helvetica 12")
        self.distance_entry.pack(pady=5)

        self.angle_label = tk.Label(new_window, text="Angle de rotation (en degrés):", font="Helvetica 12")
        self.angle_entry = tk.Entry(new_window, font="Helvetica 12")

        # Cacher l'angle par défaut
        self.angle_label.pack_forget()
        self.angle_entry.pack_forget()

        # Cacher les champs direction et distance pour ROTATE
        def update_action_fields(event):
            if self.action_choice.get() == "Move":
                self.direction_label.pack(pady=5)
                self.direction_entry.pack(pady=5)
                self.distance_label.pack(pady=5)
                self.distance_entry.pack(pady=5)
                # Cacher l'angle
                self.angle_label.pack_forget()
                self.angle_entry.pack_forget()
            elif self.action_choice.get() == "Rotate":
                self.direction_label.pack_forget()
                self.direction_entry.pack_forget()
                self.distance_label.pack_forget()
                self.distance_entry.pack_forget()
                # Afficher l'angle
                self.angle_label.pack(pady=5)
                self.angle_entry.pack(pady=5)

        # Lier la mise à jour des champs à la sélection du menu déroulant
        self.action_choice.bind("<<ComboboxSelected>>", update_action_fields)

        # Frame pour le bouton, positionné en bas
        button_frame = tk.Frame(new_window)
        button_frame.pack(side="bottom", pady=10)

        # Bouton pour envoyer l'action via MQTT
        tk.Button(button_frame, text="Envoyer Action", font="Helvetica 12 bold", bg="#28a745", fg="white",
                  relief="groove", command=self.send_action).pack()

    def send_action(self):
        action = self.action_choice.get()
        topic = self.topic.get()
        if topic:
            if action == "Move":
                direction = self.direction_entry.get()
                distance = int(self.distance_entry.get())
                json_message = json.dumps({
                    "name": action,
                    "params": {
                        "direction": direction,
                        "distance_cm": distance
                    }
                })
            elif action == "Rotate":
                angle = int(self.angle_entry.get())
                json_message = json.dumps({
                    "name": action,
                    "params": {
                        "angle": angle
                    }
                })

            # Publier le message JSON sur le topic
            self.client.publish(topic, json_message)
            self.log_message(f"Action '{json_message}' envoyée sur le topic {topic}")
        else:
            self.log_message("Erreur : Le topic n'est pas défini.")


# Création de l'interface Tkinter
root = tk.Tk()
app = MQTTApp(root)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)
root.mainloop()
