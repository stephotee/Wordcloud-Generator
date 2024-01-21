import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import ImageColor

# Function to change the casing of words based on user selection
def change_case(text, case):
    if case == "All upper case":
        return text.upper()
    else:  # All lower case by default
        return text.lower()

# Function to generate word cloud with padding and case options
def generate_wordcloud(text, max_words, color_func, text_case):
    wordcloud = WordCloud(width=800,
                          height=400,
                          max_font_size=75,
                          max_words=max_words,
                          background_color='white',
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

# Determine the color function based on the color profile chosen by the user
def get_color_func(profile):
    if profile == "Black text, white background":
        return lambda *args, **kwargs: "#000000"
    elif profile == "White text, black background":
        return lambda *args, **kwargs: "#FFFFFF"
    elif profile == "Multi-colour text, white background":
        colors = ['#0F1035', '#365486', '#7FC7D9', '#DCF2F1']
        return lambda *args, **kwargs: colors[np.random.randint(0, len(colors))]
    elif profile == "Multi-colour text, black background":
        colors = ['#FC993C', '#FFE775', '#BD4682', '#8C2057']
        return lambda *args, **kwargs: colors[np.random.randint(0, len(colors))]

color_func = get_color_func(color_choice)

if st.button("Generate Word Cloud"):
    # Filter out additional stopwords
    for stopword in additional_stopwords:
        user_input = user_input.replace(stopword, "")

    # Transform text based on user choice for case
    processed_text = change_case(user_input, case_choice)
    
    # Generate word cloud
    generate_wordcloud(processed_text, max_words, color_func, case_choice)
