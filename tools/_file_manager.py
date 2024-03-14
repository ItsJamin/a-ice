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


def create_and_save_image(canvas, width, height, label, dataset, ending=".png", training_data=True):
    # Assuring that Folders are generated correctly
    if training_data:
        file_path = os.path.join(os.getcwd(), PATH_TO_IMAGES, f"{dataset}_{width}_{height}", "train",label)
    else:
        file_path = os.path.join(os.getcwd(), PATH_TO_IMAGES,f"{dataset}_{width}_{height}", "test/test") #saves in test folder
    
    create_folder(file_path)

    # Recreating Image
    postscript = canvas.postscript(colormode="color")
    image = Image.open(io.BytesIO(postscript.encode("utf-8")))
    
    image_index = len(os.listdir(file_path))
    print(f"Index of {label}: {image_index}")
    image.save(os.path.join(file_path, f"{image_index}.png"))
    #image.show()


# Function for creating a folder if it does not exist
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
    return path
