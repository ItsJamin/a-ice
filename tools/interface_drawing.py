import random
import tkinter as tk
import _file_manager as files
import _canvas_draw as cdraw

themes = "shapes_simple" # change for other datasets (shapes_simple, letters_small)
_width, _height = 256, 256
_MAX_WIDTH, _MAX_HEIGHT = 1024, 576

concepts_to_draw = []

# Drawing Variables
pencil_size = 8


#--- (Event)-Functions ---#

def _update_canvas_size():
    global _width, _height
    try:
        new_width = int(width_entry.get())
        new_height = int(height_entry.get())
        if new_width > 0 and new_height > 0:
            _width, _height = min(_MAX_WIDTH,new_width), min(_MAX_HEIGHT,new_height)
            canvas.config(width=_width, height=_height)
    except ValueError:
        pass  # Ignore non-integer input

def _save_image(event = None):
    if chosen_theme.get() is not None:
        files.create_and_save_image(canvas, _width, _height, chosen_theme.get(), themes, ending=".png")
        canvas.delete("all")

def _skip_theme():
    chosen_theme.set(random.choice(concepts_to_draw))

def _debug_input(event):
    pass #print(event.num)


#--- Creating Interface ---#

root = tk.Tk()
root.title("Draw Program")

concepts_to_draw = files.load_list(themes)  # load labels to draw images to
chosen_theme = tk.StringVar(value="")
_skip_theme()

theme_label = tk.Label(root, textvariable=chosen_theme)
theme_label.pack()

canvas = cdraw.get_canvas(root, _width, _height)
canvas.pack()

size_frame = tk.Frame(root)
size_frame.pack(pady=10)

width_label = tk.Label(size_frame, text="Width:")
width_label.grid(row=0, column=0, padx=5)

width_entry = tk.Entry(size_frame)
width_entry.grid(row=0, column=1, padx=5)

height_label = tk.Label(size_frame, text="Height:")
height_label.grid(row=0, column=2, padx=5)

height_entry = tk.Entry(size_frame)
height_entry.grid(row=0, column=3, padx=5)

update_button = tk.Button(size_frame, text="Change Size", command=_update_canvas_size)
update_button.grid(row=0, column=4, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

skip_button = tk.Button(button_frame, text="Skip Topic", command=_skip_theme)
skip_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save", command=_save_image)
save_button.pack(side=tk.RIGHT, padx=5)

clear_button = tk.Button(button_frame, text="Clear Canvas", command=lambda: cdraw._clear_canvas(canvas))
clear_button.pack(side=tk.LEFT, padx=5)

# Event Binding

root.bind("<Button>", _debug_input)
root.bind('<Return>', _save_image)  # Enter to save image

#gives extra parameters through lambda function to cdraw functions
canvas.bind("<B1-Motion>", lambda event: cdraw._draw(event, canvas, pencil_size)) 
canvas.bind("<ButtonPress-1>", lambda event: cdraw._draw(event, canvas, pencil_size))
canvas.bind("<ButtonRelease-1>", lambda event: cdraw._stop_draw(canvas))
canvas.bind("<B3-Motion>", lambda event: cdraw._draw(event, canvas, pencil_size*2, "white"))  # Right-click to erase
canvas.bind("<ButtonPress-3>", lambda event: cdraw._draw(event, canvas, pencil_size*2, "white"))
canvas.bind("<ButtonRelease-3>", lambda event: cdraw._stop_draw(canvas))


# Start the Interface Loop

root.mainloop()
