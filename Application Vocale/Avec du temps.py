import tkinter as tk
import speech_recognition as sr
import threading


# Fonction de reconnaissance vocale
def ecouter_microphone():
    # Initialiser le recognizer
    recognizer = sr.Recognizer()

    # Utiliser le microphone comme source audio
    with sr.Microphone() as source:
        status_label.config(text="Parlez maintenant...", bg="#F8D7DA", fg="#721C24")
        root.update_idletasks()  # Mettre à jour l'interface avant d'écouter
        print("Parlez maintenant...")  # Affiche dans la console

        # Ajuster le niveau de bruit ambiant
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            # Écouter l'audio depuis le microphone
            audio = recognizer.listen(source, timeout=5)

            # Reconnaître le texte avec l'API Google (requiert Internet)
            texte = recognizer.recognize_google(audio, language="fr-FR")
            print("Vous avez dit :", texte)  # Affiche dans la console
            result_label.config(text=f"Vous avez dit : {texte}", fg="#155724", bg="#D4EDDA")

        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que vous avez dit.")  # Affiche dans la console
            result_label.config(text="Je n'ai pas compris ce que vous avez dit.", fg="#721C24", bg="#F8D7DA")
        except sr.RequestError:
            print("Erreur de connexion à l'API de reconnaissance vocale.")  # Affiche dans la console
            result_label.config(text="Erreur de connexion à l'API.", fg="#721C24", bg="#F8D7DA")
        except sr.WaitTimeoutError:
            print("Temps d'attente dépassé. Veuillez réessayer.")  # Affiche dans la console
            result_label.config(text="Temps d'attente dépassé. Veuillez réessayer.", fg="#721C24", bg="#F8D7DA")

        # À la fin de l'écoute, changer l'étiquette pour indiquer que l'enregistrement est terminé
        status_label.config(text="Enregistrement fini", bg="#D4EDDA", fg="#155724")
        root.update_idletasks()  # Mettre à jour l'interface


# Fonction pour démarrer la reconnaissance vocale dans un nouveau thread
def lancer_reconnaissance():
    thread = threading.Thread(target=ecouter_microphone)
    thread.start()


# Créer la fenêtre principale
root = tk.Tk()
root.title("Reconnaissance Vocale")

# Dimensions de la fenêtre
root.geometry("400x300")
root.config(bg="#E9ECEF")

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
