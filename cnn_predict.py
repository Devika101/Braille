import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

IMG_SIZE = 28  # or size you trained your model with
model = load_model("braille_model.h5")  # your trained model

def predict_braille_cell(img_path):
    """Predict a single Braille character from an image"""
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE), color_mode='grayscale')
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    char_index = np.argmax(prediction)
    return chr(65 + char_index)  # 0=A, 1=B, etc.
