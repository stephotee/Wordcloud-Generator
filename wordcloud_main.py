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

# Function to change the casing of words based on user selection
def change_case(text, case):
    if case == "All upper case":
        return text.upper()
    else:  # All lower case by default
        return text.lower()

# Function to generate word cloud with padding and case options
def generate_wordcloud(text, max_words, color_func, word_padding, text_case):
    wordcloud = WordCloud(width=800,
                          height=400,
                          max_font_size=75,
                          max_words=max_words,
                          background_color='white',
                          scale=word_padding,  # Adjust scale for padding between words
                          color_func=color_func,
                          prefer_horizontal=1.0).generate(text)

    # Display the generated word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

# Streamlit UI
st.title("Word Cloud Generator")
user_input = st.text_area("Paste your text here:")
max_words = st.slider("Maximum number of words", min_value=5, max_value=100, step=5, value=50)
color_choice = st.selectbox("Color Profile", ["Black text, white background", "White text, black background",
                                              "Multi-colour text, white background", "Multi-colour text, black background"])
case_choice = st.radio("Text Case", ["All lower case", "All upper case"])
additional_stopwords = [word.strip() for word in st.text_input("Enter words to exclude (separate with commas):").split(',')]

if st.button("Generate Word Cloud"):
    # Add color function based on user choice
    if color_choice == "Black text, white background":
        color_func = lambda *args, **kwargs: "#000000"
    elif color_choice == "White text, black background":
        color_func = lambda *args, **kwargs: "#FFFFFF"

    # Transform text based on user choice for case
    processed_text = change_case(user_input, case_choice)


# Stopword input
new_stopwords = [word.strip() for word in st.text_input("Enter words to exclude (separate with commas):").split(',')]


# Generate word cloud button
# if st.button("Generate Word Cloud"):
#    if user_input:
#        generate_word_cloud(user_input, max_words, color_profile, text_color, background_color, new_stopwords)
#    else:
#        st.error("Please enter some text to generate a word cloud.")


# Generate word cloud v2
    generate_wordcloud(processed_text, max_words, color_func, 1.1, case_choice)  # scale set to 1.1 for slight padding
