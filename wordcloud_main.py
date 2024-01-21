import streamlit as st
import pandas as pd
from wordcloud import WordCloud, get_single_color_func
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import io
from PIL import Image
import base64
import random

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Function to process text
def process_text(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)

# Function to get image download link
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Custom color function
def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = kwargs.get('colors', ['#FFFFFF'])
    return random.choice(colors)

# Streamlit app title
st.title("Word Cloud Generator")

# Custom CSS to set the background color to white
st.markdown(
    """
    <
