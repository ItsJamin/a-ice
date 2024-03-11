import tkinter as tk
from tkinter.simpledialog import askstring
from PIL import Image, ImageDraw
import os
import random

dataset_type = "shapes200200" # images800600 ; letters200200
theme_location = "themes/simpleshapes" # "letters_small"
_width = 200
_height = 200

themen_liste = []

def random_theme():
    return random.choice(themen_liste)

def load_themen_liste(file_path):
    with open(file_path, 'r') as file:
        themen_liste = [line.strip() for line in file.readlines()]
    return themen_liste

# Funktion zum Erstellen eines Ordners, falls er nicht existiert
def create_folder(folder_name):
    if not os.path.exists("datasets/"+dataset_type+"/"+folder_name):
        os.makedirs("datasets/"+dataset_type+"/"+folder_name)

# Initialisiere das Tkinter-Fenster
root = tk.Tk()
root.title("Zeichenprogramm")

themen_liste = load_themen_liste(theme_location) #Vorschläge was zu zeichnen ist
chosen_theme = tk.StringVar(value=random_theme())

# Erstelle ein Label für das Thema
theme_label = tk.Label(root, textvariable=chosen_theme)
theme_label.pack()


# Funktion zum Speichern des Bildes
def save_image():
    if chosen_theme.get() is not None:
        create_folder(chosen_theme.get())
        image = Image.new("L", (_width, _height), "white")
        draw = ImageDraw.Draw(image)
        for item in canvas.find_all():
            coords = canvas.coords(item)
            color = canvas.itemcget(item, "fill") 
            draw.ellipse(coords, fill=color)
        image.save(f"datasets/{dataset_type}/{chosen_theme.get()}/{len(os.listdir(f'datasets/{dataset_type}/{chosen_theme.get()}/')) + 1}.png")
        canvas.delete("all")
        #chosen_theme.set(random_theme())


# Funktion zum Überspringen des aktuellen Themas
def skip_theme():
    chosen_theme.set(random_theme())

# Erstelle ein leeres Bild
canvas = tk.Canvas(root, width=_width, height=_height, bg='white')
canvas.pack()

# Frame für die Buttons erstellen
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Variable, um festzuhalten, ob die Maus gedrückt ist
drawing = False
erasing = False
previous_coordinates = None

# Funktion zum Starten des Zeichnens
def start_draw(event):
    global drawing
    drawing = True
    x, y = event.x, event.y
    canvas.create_oval(x-4, y-4, x+4, y+4, fill='black')


# Funktion zum Beenden des Zeichnens
def stop_draw(event):
    global drawing
    drawing = False

# Funktion zum Zeichnen
def draw(event):
    if drawing:
        x, y = event.x, event.y
        canvas.create_oval(x-4, y-4, x+4, y+4, fill='black')

# Funktion zum Starten des Zeichnens
def start_erase(event):
    global erasing
    erasing = True
    x, y = event.x, event.y
    canvas.create_oval(x-8, y-8, x+8, y+8, fill='white', outline="white")


# Funktion zum Beenden des Zeichnens
def stop_erase(event):
    global erasing
    erasing = False

# Funktion zum Radieren (rechte Maustaste)
def erase(event):
    if erasing:
        x, y = event.x, event.y
        canvas.create_oval(x-8, y-8, x+8, y+8, fill='white', outline="white")

# Funktion zum Löschen des Canvas
def clear_canvas():
    canvas.delete("all")


# Ereignisse binden
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<ButtonRelease-1>", stop_draw)
canvas.bind("<B3-Motion>", erase)  # Rechtsklick zum Radieren
canvas.bind("<ButtonPress-3>", start_erase)
canvas.bind("<ButtonRelease-3>", stop_erase)
# Ereignisbindung für die Enter-Taste
root.bind('<Return>', save_image)

# Knopf zum Überspringen des Themas hinzufügen
skip_button = tk.Button(button_frame, text="Thema überspringen", command=skip_theme)
skip_button.pack(side=tk.LEFT, padx=5)

# Knopf zum Speichern hinzufügen
save_button = tk.Button(button_frame, text="Speichern", command=save_image)
save_button.pack(side=tk.RIGHT, padx=5)



# Knopf zum Löschen des Canvas hinzufügen
clear_button = tk.Button(button_frame, text="Canvas löschen", command=clear_canvas)
clear_button.pack(side=tk.LEFT, padx=5)





# Starte die Tkinter-Schleife
root.mainloop()
