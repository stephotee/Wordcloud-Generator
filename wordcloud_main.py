import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import io

# Function to choose color for the words
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    if color_profile == "Multi-colour text, white background":
        colors = ["#0F1035", "#365486", "#7FC7D9", "#DCF2F1"]
    elif color_profile == "Multi-colour text, black background":
        colors = ["#FC993C", "#FFE775", "#BD4682", "#8C2057"]
    else:
        colors = [text_color]

    return np.random.choice(colors)

# Function to generate and display word cloud
def generate_word_cloud(text, max_words, color_profile, text_color, background_color, additional_stopwords):
    wordcloud = WordCloud(width=800, height=400, max_words=max_words, 
                          background_color=background_color,
                          stopwords=STOPWORDS.union(set(additional_stopwords)),
                          color_func=lambda *args, **kwargs: color_func(*args, **kwargs),
                          prefer_horizontal=1.0).generate(text)

    # Display image
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

# Streamlit UI
st.title("Word Cloud Generator")

# Text input
user_input = st.text_area("Enter your text here:")

# Word count slider
max_words = st.slider("Max words in cloud", 5, 100, 50, 5)

# Color profile selection
color_profiles = {
    "Black text, white background": ("#000000", "#FFFFFF"),
    "White text, black background": ("#FFFFFF", "#000000"),
    "Multi-colour text, white background": ("", "#FFFFFF"),
    "Multi-colour text, black background": ("", "#000000")
}

color_profile = st.selectbox("Select Color Profile", list(color_profiles.keys()))
text_color, background_color = color_profiles[color_profile]

# Stopword input
new_stopwords = st.text_input("Enter words to exclude (separate with commas):").split(',')

# Generate word cloud button
if st.button("Generate Word Cloud"):
    if user_input:
        generate_word_cloud(user_input, max_words, color_profile, text_color, background_color, new_stopwords)
    else:
        st.error("Please enter some text to generate a word cloud.")
