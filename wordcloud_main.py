import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import base64
import io

# Function to convert color profile to corresponding colors
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    if color_profile == "Profile 1":
        return "#000000" # Black color
    elif color_profile == "Profile 2":
        colors = ["#0F1035", "#365486", "#7FC7D9", "#DCF2F1"]
    elif color_profile == "Profile 3":
        colors = ["#A94438", "#D24545", "#E6BAA3", "#E4DEBE"]
    elif color_profile == "Profile 4":
        colors = ["#4F6F52", "#739072", "#86A789", "#D2E3C8"]
    elif color_profile == "Profile 5":
        colors = ["#FC993C", "#FFE775", "#BD4682", "#8C2057"]
    return np.random.choice(colors)

# Streamlit UI
st.title("Word Cloud Generator")

# Text input
user_input = st.text_area("Enter your text here:")

# Word count slider
max_words = st.slider("Max words in cloud", 1, 100, 50)

# Color profile selection
color_profile = st.selectbox("Select Color Profile", 
                             ["Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5"])

# Generate word cloud button
if st.button("Generate Word Cloud"):
    if user_input:
        wordcloud = WordCloud(width=800, height=400, max_words=max_words, color_func=color_func, prefer_horizontal=1.0).generate(user_input)

        # Display image
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        # Convert to PNG
        img_data = io.BytesIO()
        wordcloud.to_image().save(img_data, format="PNG")
        img_data.seek(0)

        # Download link
        btn = st.download_button(label="Download Image", data=img_data, file_name="wordcloud.png", mime="image/png")
    else:
        st.error("Please enter some text to generate a word cloud.")
