import os
from PIL import Image, ImageDraw, ImageGrab
import io

PATH_TO_LIST = "data/lists/"
PATH_TO_IMAGES = "data/images/"

def load_list(label):
    file_path = os.path.join(os.getcwd(), PATH_TO_LIST, label)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []


def create_and_save_image(canvas, width, height, label, dataset, ending=".png", save = True):
    # Recreating Image
    image = create_image(canvas)

    save_image(image, width, height, label, dataset, ending)
    
    return image


def create_image(canvas):
    postscript = canvas.postscript(colormode="color")
    image = Image.open(io.BytesIO(postscript.encode("utf-8")))
    return image

def save_image(image, width, height, label, dataset, ending):
    # Assuring that Folders are generated correctly
    file_path = os.path.join(os.getcwd(), PATH_TO_IMAGES, f"{dataset}_{width}_{height}", label)
    create_folder(file_path)
    
    image_index = len(os.listdir(file_path))
    print(f"Index of {label}: {image_index}")
    image.save(os.path.join(file_path, f"{image_index}.png"))


# Function for creating a folder if it does not exist
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
    return path
