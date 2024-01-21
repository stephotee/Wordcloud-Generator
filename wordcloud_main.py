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
    <style>
    .reportview-container {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Text input
text_input = st.text_area("Enter text (comma separated)", "")

# File upload
uploaded_file = st.file_uploader("Or upload a text (.txt) or CSV file", type=['txt', 'csv'])

# Font selection
font_choice = st.selectbox("Choose a font", ["Tahoma", "Calibri", "Helvetica", "Arial", "Verdana", "Times New Roman"])

# Max words control
max_words = st.slider("Select max number of words", 1, 100, 50)

# Color profile selection
color_profiles = {
    "Profile 1": ["#000000"],
    "Profile 2": ["#0F1035", "#365486", "#7FC7D9", "#DCF2F1"],
    "Profile 3": ["#A94438", "#D24545", "#E6BAA3", "#E4DEBE"],
    "Profile 4": ["#4F6F52", "#739072", "#86A789", "#D2E3C8"],
    "Profile 5": ["#FC993C", "#FFE775", "#BD4682", "#8C2057"]
}
color_choice = st.selectbox("Choose a color profile", list(color_profiles.keys()))

# Initialize processed_text
processed_text = ""

# Generate button
if st.button("Generate Word Cloud"):
    if uploaded_file is not None:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            text = ' '.join(row[0] for row in df.values)
        else:
            text = str(uploaded_file.read(), 'utf-8')

        processed_text = process_text(text)

    elif text_input:
        processed_text = process_text(text_input)

    if processed_text:
        wordcloud = WordCloud(width=800, height=400, max_font_size=75, max_words=max_words, font_path=font_choice, 
                              background_color='white', prefer_horizontal=1.0, 
                              color_func=lambda *args, **kwargs: custom_color_func(*args, **kwargs, colors=color_profiles[color_choice])).generate(processed_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        # Convert plot to PNG image
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        st.markdown(get_image_download_link(Image.open(img_buf), 'wordcloud.png', 'Download Word Cloud as PNG'), unsafe_allow_html=True)

