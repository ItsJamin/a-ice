import os
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras import layers
from keras.models import Sequential
import random
from datetime import datetime

PATH_TO_IMAGES = "data/images/"
PATH_TO_TEST_IMAGES = "data/test_images/"
PATH_TO_MODELS = "data/trained_models/"

dataset_name = "shapes_simple_256_256"
data_dir = os.path.join(PATH_TO_IMAGES, dataset_name)
test_dir = os.path.join(PATH_TO_TEST_IMAGES, dataset_name)
width, height = 256, 256

train_ds, val_ds, test_ds = None, None, None
model = None

#--- Preprocessing of Images ---#

def get_datasets(seed = 123, batch_size = 10):

    # Generate seed
    # (needs to be same for train_ds and val_ds to properly divde images)

    if seed == 0: # Input 0 to get random seed, leave blank for set one
        seed = random.randint(0, 999)
    

    train_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=seed,
        image_size=(height, width),
        batch_size=batch_size)

    val_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=seed,
        image_size=(height, width),
        batch_size=batch_size)
    
    test_ds = keras.utils.image_dataset_from_directory(
        test_dir,
        seed=seed,
        image_size=(height, width),
        batch_size=batch_size)
    

    return train_ds, val_ds, test_ds

def visualize_training_process(history, epochs):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

def train_model(epochs):

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    return history

def create_model():
    model = Sequential([
        layers.Rescaling(1./255, input_shape=(height, width, 3)), #first layers normalizes pixel (0-255) -> (0.0->1.0)
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='sigmoid'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='relu')
    ])

    # Create model
    model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


    return model


def open_model(name):
    return keras.models.load_model(os.path.join(PATH_TO_MODELS,name))

def save_model():
    date = datetime.today().strftime('%Y-%m-%d')
    model.save(os.path.join(PATH_TO_MODELS,f'acorn_{date}.keras'))

def evaluate_model(model, test_ds):
    # Evaluate the model on the test dataset
    test_loss, test_accuracy = model.evaluate(test_ds)
    print(f"Test Accuracy: {test_accuracy}")
    print(f"Test Loss: {test_loss}")

#--- Execution ---#

batch_size = 100
epochs = 2000

if __name__ == "__main__":

    # Create data
    
    train_ds, val_ds, test_ds = get_datasets(0, batch_size)

    class_names = train_ds.class_names

    num_classes = len(class_names)

    # Some magic for better perfomance

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Create model
    model = create_model()
    model.summary()

    # Train the modes

    history = train_model(epochs)

    evaluate_model(model, test_ds)

    visualize_training_process(history, epochs)

    save_model()
    

