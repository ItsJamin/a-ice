import tkinter as tk
import _file_manager as files
import _canvas_draw as cdraw
import tensorflow as tf
import matplotlib.pyplot as plt
import keras
import os
import numpy as np
from PIL import Image

model_path = "data/trained_models/acorn_2024-03-17.keras"
dataset_path = "data/images/shapes_simple_256_256"
model = keras.models.load_model(os.path.join(os.getcwd(),model_path))
print(model.summary())
class_names = os.listdir(dataset_path)
print(class_names)

_width, _height = 256, 256
_MAX_WIDTH, _MAX_HEIGHT = 1024, 576

# Drawing Variables
pencil_size = 8

#--- (Event)-Functions ---#

def _get_model_prediction():

    image = files.create_image(canvas)
    #image = Image.open(os.path.join(os.getcwd(),dataset_path,"circle/69.png"))
    processed_image = preprocess_test_image(image)

    predictions = model.predict(processed_image[None,:,:])
    print(predictions)

    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]

    output_label.config(text=predicted_class)

def preprocess_test_image(image, target_size=(256, 256)):    
    image = image.resize(target_size)   
    reshaped_image = np.array(image)
    return reshaped_image

def _reset():
    cdraw._clear_canvas(canvas) 
    output_label.config(text="")

#--- Creating Interface ---#

root = tk.Tk()
root.title("Test Model Program")

canvas = cdraw.get_canvas(root, _width, _height)
canvas.pack()

prediction_label = tk.Label(root, text="Model classifies images as: ")
prediction_label.pack(pady=5)

output_label = tk.Label(root, text="")
output_label.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

submit_button = tk.Button(button_frame, text="Submit to Model", command=_get_model_prediction)
submit_button.pack(side=tk.RIGHT, padx=5)

clear_button = tk.Button(button_frame, text="Clear Canvas", command=_reset)
clear_button.pack(side=tk.LEFT, padx=5)

# Event Binding

root.bind('<Return>', lambda event: _get_model_prediction())

#gives extra parameters through lambda function to cdraw functions
canvas.bind("<B1-Motion>", lambda event: cdraw._draw(event, canvas, pencil_size)) 
canvas.bind("<ButtonPress-1>", lambda event: cdraw._draw(event, canvas, pencil_size))
canvas.bind("<ButtonRelease-1>", lambda event: cdraw._stop_draw(canvas))
canvas.bind("<B3-Motion>", lambda event: cdraw._draw(event, canvas, pencil_size*2, "white"))  # Right-click to erase
canvas.bind("<ButtonPress-3>", lambda event: cdraw._draw(event, canvas, pencil_size*2, "white"))
canvas.bind("<ButtonRelease-3>", lambda event: cdraw._stop_draw(canvas))


# Start the Interface Loop
root.mainloop()