import tkinter as tk
import speech_recognition as sr

# Fonction de reconnaissance vocale
def ecouter_microphone():
    # Initialiser le recognizer
    recognizer = sr.Recognizer()

    # Utiliser le microphone comme source audio
    with sr.Microphone() as source:
        # Modifier l'interface pour dire à l'utilisateur de parler
        status_label.config(text="Parlez maintenant...", bg="#F8D7DA", fg="#721C24")
        print("Parlez maintenant...")

        # Ajuster le niveau de bruit ambiant
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            # Écouter l'audio depuis le microphone sans timeout
            audio = recognizer.listen(source)

            # Reconnaître le texte avec l'API Google (requiert Internet)
            texte = recognizer.recognize_google(audio, language="fr-FR")
            print("Vous avez dit :", texte)
            result_label.config(text=f"Vous avez dit : {texte}", fg="#155724", bg="#D4EDDA")

        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que vous avez dit.")
            result_label.config(text="Je n'ai pas compris ce que vous avez dit.", fg="#721C24", bg="#F8D7DA")
        except sr.RequestError:
            print("Erreur de connexion à l'API de reconnaissance vocale.")
            result_label.config(text="Erreur de connexion à l'API.", fg="#721C24", bg="#F8D7DA")

# Fonction pour démarrer l'enregistrement lorsque l'utilisateur maintient le bouton
def start_enregistrement(event):
    """Démarre l'enregistrement vocal lorsqu'on appuie sur le bouton."""
    # Modifier le texte du bouton et du statut avant de commencer l'enregistrement
    status_label.config(text="Parlez maintenant...", bg="#F8D7DA", fg="#721C24")
    start_button.config(text="Relâchez pour arrêter", bg="#DC3545")  # Le bouton devient rouge pour "Relâcher"

    # Appeler la fonction d'enregistrement
    ecouter_microphone()

# Fonction pour arrêter l'enregistrement lorsque l'utilisateur relâche le bouton
def stop_enregistrement(event):
    """Arrête l'enregistrement et affiche le texte reconnu."""
    status_label.config(text="Enregistrement arrêté.", bg="#D1ECF1", fg="#0C5460")
    start_button.config(text="Démarrer", bg="#007BFF")  # Le bouton revient à son état initial

# Créer la fenêtre principale
root = tk.Tk()
root.title("Reconnaissance Vocale")

# Dimensions de la fenêtre
root.geometry("400x300")
root.config(bg="#E9ECEF")

# Ajouter un label de statut avec un fond coloré
status_label = tk.Label(root, text="Cliquez sur 'Démarrer' pour parler", font=("Helvetica", 14), bg="#D1ECF1", fg="#0C5460", relief="solid", padx=10, pady=10)
status_label.pack(pady=20)

# Ajouter un bouton pour démarrer la reconnaissance vocale
start_button = tk.Button(root, text="Démarrer", font=("Helvetica", 14), bg="#007BFF", fg="white", relief="flat", height=2, width=15)
start_button.pack(pady=10)

# Ajouter un label pour afficher le texte reconnu
result_label = tk.Label(root, text="", font=("Helvetica", 12), wraplength=300, bg="#FFFFFF", fg="#333333", relief="sunken", padx=10, pady=10)
result_label.pack(pady=20)

# Lier les événements de pression et de relâchement du bouton
start_button.bind("<ButtonPress-1>", start_enregistrement)  # Quand le bouton est pressé
start_button.bind("<ButtonRelease-1>", stop_enregistrement)  # Quand le bouton est relâché

# Démarrer l'interface graphique
root.mainloop()
