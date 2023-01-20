import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import requests

@st.cache
def get_prediction_single_image(model, directory):
    
    img = tf.keras.preprocessing.image.load_img(directory, target_size=(224, 224, 3))
    plt.imshow(img)
    plt.axis("off")

    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    prediction = model.predict(img_array)
    score = tf.nn.softmax(prediction[0])

    return class_names[np.argmax(score)]


class_names = ['Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal',
               'Broccoli', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower',
               'Cucumber', 'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato']


@st.cache(allow_output_mutation=True)
def load_model():
    path = os.path.dirname(__file__)
    my_file = path+'my_model/saved_model.pb'
    model = tf.keras.models.load_model(my_file, compile=False)
    return model


# model = load_model()

@st.cache
def get_image(url):
    img = requests.get(url)
    file = open('sample_image.jpg', 'wb')
    file.write(img.content)
    file.close()
    img_file_name = 'sample_image.jpg'
    return img_file_name

st.title('Vegetable Classification')
st.write('Add image url from the source page')

url = st.text_input("Enter Image Url:")
if url:
    image = get_image(url)
    st.image(image)
    Classify = st.button("Classify Image")
    if Classify:
        st.write("")
        st.write("Classifying...")
        label = get_prediction_single_image(load_model(), image)
        st.write(str(label))
else:
    st.write("Paste Image URL")

