import os
import cv2
import time

# Nom du package de jeu
GAME_PACKAGE_NAME = "com.dts.freefireth"

# 1. Vérifiez le jeu
def is_game_running():
    output = os.popen("adb shell dumpsys activity | findstr mCurrentFocus").read()
    return GAME_PACKAGE_NAME in output

# 2. Capture d'écran du téléphone
def capture_screen():
    os.system("adb exec-out screencap -p > screen.png")
    print("Capture d'écran !")

# 3. Recherche de l'ennemi (analyse d'écran)
def find_enemy():
    screenshot = cv2.imread("screen.png", 0)  # Télécharger une capture d'écran
    template = cv2.imread("head_template.png", 0)  # Télécharger l'image d'en-tête

    # Assurez-vous de télécharger les images.
    if screenshot is None or template is None:
        print("Erreur: les images n'ont pas été chargées correctement.!")
        return None

    # Trouver une correspondance
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Si l'ennemi est trouvé
    if max_val > 0.7:  # Il s'agit du pourcentage correspondant 0.7
        print(f"Ennemi trouvé avec pourcentage de correspondance: {max_val}")
        return max_loc  # Coordonnées ennemies
    else:
        return None

# 4. Simuler un tir en visant un tir à la tête
def shoot_at_head(enemy_location):
    if enemy_location:
        x, y = enemy_location
        
        # Simuler le tapotement de l'écran dans les coordonnées de la tête

        os.system(f"adb shell input touchscreen swipe 1552 453 { x} { y }  ")
        os.system(f"adb shell input tap 1980 750 ")
        os.system(f"adb shell input tap 1980 750 ")


        print(f"Une balle dans la tête: {x}, {y}")
    else:
        print("Ennemi non trouvé !")

# 5. Relier les étapes entre elles
if __name__ == "__main__":
    while True:
        # Vérifiez le jeu
        if is_game_running():
            print("Le jeu est en cours d'exécution...")

            capture_screen()

            enemy_location = find_enemy()

            if enemy_location:
                shoot_at_head(enemy_location)
        else:
            print("Le jeu ne fonctionne pas, en attente...")

        time.sleep(0.1)
