import tkinter as tk

# drawing logic
previous_point, current_point = [0,0],[0,0]

def get_canvas(root, _width, _height, bg_color = "white"):
    canvas = tk.Canvas(root, width=_width, height=_height, bg='white')
    return canvas


def _stop_draw(event):
    global previous_point
    previous_point = [0,0]


def _draw(event, canvas, size = 8, color = "black"):
    global previous_point, current_point

    current_point = [event.x, event.y]
    
    if previous_point != [0,0]:
        x, y = event.x, event.y
        #canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='black')
        canvas.create_line(previous_point[0],previous_point[1],current_point[0],current_point[1], 
                           fill=color, width=size, capstyle=tk.ROUND, joinstyle=tk.BEVEL)
    
    previous_point = current_point


def _clear_canvas(canvas):
    canvas.delete("all")