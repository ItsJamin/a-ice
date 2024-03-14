import random
import tkinter as tk
import sys
sys.path.append('../file_tool/')
import _file_manager as files

themes = "shapes_simple" # change for other datasets (shapes_simple, letters_small)
_width, _height = 256, 256
_MAX_WIDTH, _MAX_HEIGHT = 1024, 576

concepts_to_draw = []

# Variables to record whether the mouse is pressed
pencil_size = 8
previous_point, current_point = [0,0], [0,0]

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

def _stop_draw(event):
    global previous_point
    previous_point = [0,0]

def _draw(event, color, size = pencil_size):
    global previous_point, current_point

    current_point = [event.x, event.y]
    
    if previous_point != [0,0]:
        x, y = event.x, event.y
        #canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='black')
        canvas.create_line(previous_point[0],previous_point[1],current_point[0],current_point[1], 
                           fill=color, width=size, capstyle=tk.ROUND, joinstyle=tk.BEVEL)
    
    previous_point = current_point

def _erase(event):
    global previous_point, current_point
    current_point = [event.x, event.y]
    
    if previous_point != [0,0]:
        x, y = event.x, event.y
        canvas.create_line(previous_point[0],previous_point[1],current_point[0],current_point[1], 
                           fill="white", width=pencil_size, capstyle=tk.ROUND, joinstyle=tk.BEVEL)
    
    previous_point = current_point

def _clear_canvas():
    canvas.delete("all")

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

canvas = tk.Canvas(root, width=_width, height=_height, bg='white')
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

clear_button = tk.Button(button_frame, text="Clear Canvas", command=_clear_canvas)
clear_button.pack(side=tk.LEFT, padx=5)

# Event Binding
root.bind("<Button>", _debug_input)
canvas.bind("<B1-Motion>", lambda event: _draw(event, "black")) #gives extra parameters (color) through lambda function
canvas.bind("<ButtonPress-1>", lambda event: _draw(event, "black"))
canvas.bind("<ButtonRelease-1>", _stop_draw)
canvas.bind("<B3-Motion>", lambda event: _draw(event, "white", pencil_size*2))  # Right-click to erase
canvas.bind("<ButtonPress-3>", lambda event: _draw(event, "white", pencil_size*2))
canvas.bind("<ButtonRelease-3>", _stop_draw)
root.bind('<Return>', _save_image)  # Enter to save image

# Start the Interface Loop

root.mainloop()
