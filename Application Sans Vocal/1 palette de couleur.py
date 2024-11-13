import tkinter as tk
from tkinter import ttk, messagebox
import paho.mqtt.client as mqtt
import json
import base64
import binascii

class MQTTApp:
    def __init__(self, root, language="English"):
        self.language = language  # Store the selected language
        self.root = root
        self.root.title(self.get_text("mqtt_app_title"))
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")  # Gris très clair pour l'arrière-plan principal
        self.root.option_add("*Font", "Helvetica 12")

        # Frame for connection configuration
        self.config_frame = tk.Frame(root, bg="#d3dce6", padx=10, pady=10, relief="ridge",
                                     bd=2)  # Gris clair pour le cadre de configuration
        self.config_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Labels and entry fields for broker configuration
        self.add_label_and_entry(self.config_frame, self.get_text("mqtt_broker_address"), 0, "broker_ip")
        self.add_label_and_entry(self.config_frame, self.get_text("mqtt_port"), 1, "broker_port", default="1883")
        self.add_label_and_entry(self.config_frame, self.get_text("mqtt_topic"), 2, "topic")
        self.add_label_and_entry(self.config_frame, self.get_text("mqtt_username"), 3, "username")
        self.add_label_and_entry(self.config_frame, self.get_text("mqtt_password"), 4, "password", show="*")

        # Log display frame
        self.log_frame = tk.LabelFrame(root, text=self.get_text("log_title"), bg="#f0f4f8", font="Helvetica 12 bold",
                                       padx=10, pady=10)
        self.log_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        self.msg_box = tk.Text(self.log_frame, height=10, width=50, state='disabled', bg="#ffffff",
                               fg="#333333")  # Blanc pour les logs, gris foncé pour le texte
        self.msg_box.pack(expand=True, fill="both")

        # Message input field
        self.message_label = tk.Label(root, text=self.get_text("message_label"), bg="#f0f4f8", font="Helvetica 12 bold")
        self.message_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # Larger text field for message input
        self.message_entry = tk.Text(root, height=2, width=30, font="Helvetica 12")
        self.message_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

        # Dropdown for message type
        self.message_type_label = tk.Label(root, text=self.get_text("message_type_label"), bg="#f0f4f8",
                                           font="Helvetica 12 bold")
        self.message_type_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.message_type = ttk.Combobox(root, values=["Text", "JSON", "BASE64", "Hex", "CBOR"], state="readonly")
        self.message_type.current(0)
        self.message_type.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

        # Buttons
        self.connect_button = tk.Button(root, text=self.get_text("connect_button"), command=self.connect_to_broker,
                                        bg="#005a9e",
                                        fg="white", font="Helvetica 12 bold",
                                        relief="groove")  # Bleu foncé pour le bouton de connexion
        self.connect_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.send_button = tk.Button(root, text=self.get_text("send_message_button"), command=self.send_message,
                                     bg="#28a745", fg="white",
                                     font="Helvetica 12 bold", relief="groove")  # Vert pour le bouton d'envoi
        self.send_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Button to open a new window
        self.new_window_button = tk.Button(root, text=self.get_text("robot_action_button"),
                                           command=self.open_new_window,
                                           bg="#dc3545", fg="white", font="Helvetica 12 bold",
                                           relief="groove")  # Rouge pour le bouton d'action robot
        self.new_window_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # MQTT client configuration
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def get_text(self, key):
        """Return the corresponding text for the selected language"""
        texts = {
            "English": {
                "mqtt_app_title": "MQTT Application",
                "mqtt_broker_address": "MQTT Broker Address:",
                "mqtt_port": "Port (default 1883):",
                "mqtt_topic": "Topic:",
                "mqtt_username": "Username:",
                "mqtt_password": "Password:",
                "log_title": "Logs",
                "message_label": "Message to send:",
                "message_type_label": "Message type:",
                "connect_button": "Connect",
                "send_message_button": "Send Message",
                "robot_action_button": "Robot Action",
            },
            "French": {
                "mqtt_app_title": "Application MQTT",
                "mqtt_broker_address": "Adresse du serveur MQTT :",
                "mqtt_port": "Port (par défaut 1883) :",
                "mqtt_topic": "Sujet :",
                "mqtt_username": "Nom d'utilisateur :",
                "mqtt_password": "Mot de passe :",
                "log_title": "Logs",
                "message_label": "Message à envoyer :",
                "message_type_label": "Type de message :",
                "connect_button": "Se connecter",
                "send_message_button": "Envoyer le message",
                "robot_action_button": "Action Robot",
            },
        }
        return texts[self.language].get(key, key)

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
            self.log_message("Successfully connected to the MQTT broker!")
            client.subscribe(userdata['topic'])
        else:
            self.log_message("Connection failed, return code: " + str(rc))

    def on_message(self, client, userdata, msg):
        self.log_message(f"Message received on {msg.topic}: {msg.payload.decode()}")

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
                self.log_message(f"Message sent to {topic} [{message_type}]: {payload}")
            except (json.JSONDecodeError, binascii.Error) as e:
                self.log_message(f"Error: Unable to send the message ({e})")
                messagebox.showerror("Error", f"Incorrect message format for {message_type}")
        else:
            self.log_message("Error: You must enter a message and a topic.")

    def log_message(self, message):
        self.msg_box.config(state='normal')
        self.msg_box.insert(tk.END, message + '\n')
        self.msg_box.yview(tk.END)
        self.msg_box.config(state='disabled')

    def open_new_window(self):
        # Create a new window
        new_window = tk.Toplevel(self.root)
        new_window.title("Actions - MQTT")
        new_window.geometry("400x400")

        # Label for action choice
        tk.Label(new_window, text="Choose an action:", font="Helvetica 12 bold").pack(pady=10)

        # Dropdown menu for actions MOVE, ROTATE, etc.
        self.action_choice = ttk.Combobox(new_window,
                                          values=["Move", "Rotate", "Pickup", "Place", "Putback", "Position"],
                                          state="readonly", font="Helvetica 12")
        self.action_choice.current(0)  # Default to Move
        self.action_choice.pack(pady=10)

        # Fields for direction, distance, and angle
        self.direction_label = tk.Label(new_window, text="Direction (left/right):", font="Helvetica 12")
        self.direction_label.pack(pady=5)
        self.direction_entry = tk.Entry(new_window, font="Helvetica 12")
        self.direction_entry.pack(pady=5)

        self.distance_label = tk.Label(new_window, text="Distance in cm:", font="Helvetica 12")
        self.distance_label.pack(pady=5)
        self.distance_entry = tk.Entry(new_window, font="Helvetica 12")
        self.distance_entry.pack(pady=5)

        self.angle_label = tk.Label(new_window, text="Rotation angle (in degrees):", font="Helvetica 12")
        self.angle_entry = tk.Entry(new_window, font="Helvetica 12")

        # Hide the angle field by default
        self.angle_label.pack_forget()
        self.angle_entry.pack_forget()

        # Hide direction and distance fields for ROTATE
        def update_action_fields(event):
            if self.action_choice.get() == "Move":
                self.direction_label.pack(pady=5)
                self.direction_entry.pack(pady=5)
                self.distance_label.pack(pady=5)
                self.distance_entry.pack(pady=5)
                # Hide angle
                self.angle_label.pack_forget()
                self.angle_entry.pack_forget()
            elif self.action_choice.get() == "Rotate":
                self.direction_label.pack_forget()
                self.direction_entry.pack_forget()
                self.distance_label.pack_forget()
                self.distance_entry.pack_forget()
                # Show angle
                self.angle_label.pack(pady=5)
                self.angle_entry.pack(pady=5)

        # Bind the update of fields to the dropdown selection
        self.action_choice.bind("<<ComboboxSelected>>", update_action_fields)

        # Frame for the button, positioned at the bottom
        button_frame = tk.Frame(new_window)
        button_frame.pack(side="bottom", pady=10)

        # Button to send the action via MQTT
        tk.Button(button_frame, text="Send Action", font="Helvetica 12 bold", bg="#28a745", fg="white",
                  relief="groove", command=self.send_action).pack()

        # New "Stop Robot" button
        stop_button = tk.Button(button_frame, text="Stop Robot", font="Helvetica 12 bold", bg="red", fg="white",
                                relief="groove", command=self.stop_robot)
        stop_button.pack(pady=10)

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

            # Publish the JSON message on the topic
            self.client.publish(topic, json_message)
            self.log_message(f"Action '{json_message}' sent to topic {topic}")
        else:
            self.log_message("Error: Topic is not set.")

    def stop_robot(self):
        # Create the JSON message for "Stop"
        stop_message = json.dumps({"name": "Stop"})

        # Publish the JSON message on the topic
        topic = self.topic.get()
        if topic:
            self.client.publish(topic, stop_message)
            self.log_message(f"'Stop' message sent to topic {topic}")
        else:
            self.log_message("Error: Topic is not set.")


# Language selection window
def show_language_selection():
    lang_window = tk.Tk()
    lang_window.title("Select Language")
    lang_window.geometry("300x150")

    def set_language(language):
        lang_window.destroy()
        root = tk.Tk()
        app = MQTTApp(root, language)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.mainloop()

    tk.Label(lang_window, text="Select Language", font="Helvetica 12 bold").pack(pady=10)
    language_combobox = ttk.Combobox(lang_window, values=["English", "French"], state="readonly", font="Helvetica 12")
    language_combobox.current(0)
    language_combobox.pack(pady=10)

    tk.Button(lang_window, text="OK", command=lambda: set_language(language_combobox.get()), bg="#007bff", fg="white", font="Helvetica 12 bold").pack(pady=10)

    lang_window.mainloop()

# Launch the language selection window at the start
show_language_selection()
