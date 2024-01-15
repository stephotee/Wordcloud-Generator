import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import io
from PIL import Image
import base64
import os

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

# Function to check font availability
def font_path():
    if os.path.exists('Trebuchet MS'):
        return 'Trebuchet MS'
    else:
        # Use a default font if Trebuchet MS is not available
        return None

# Streamlit app title
st.title("Word Cloud Generator")

# Text input
text_input = st.text_area("Enter text (comma separated)", "")

# File upload
uploaded_file = st.file_uploader("Or upload a text (.txt) or CSV file", type=['txt', 'csv'])

# Initialize processed_text
processed_text = ""

# Generate button
if st.button("Generate Word Cloud"):
    if uploaded_file is not None:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded
