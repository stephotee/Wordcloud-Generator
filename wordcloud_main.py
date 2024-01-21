import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from collections import Counter

# Function to choose color for the words
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    if color_profile == "Multi-colour text, white background":
        colors = ["#0F1035", "#365486", "#7FC7D9", "#DCF2F1"]
    elif color_profile == "Multi-colour text, black background":
        colors = ["#FC993C", "#FFE775", "#BD4682", "#8C2057"]
    else:
        colors = ["#000000" if color_profile == "Black text, white background" else "#FFFFFF"]
    return np.random.choice(colors)

# Function to process text and remove additional stopwords
def process_text(text, additional_stopwords):
    for word in additional_stopwords:
        STOPWORDS.add(word.strip().lower())
    return " ".join([word for word in text.split() if word.lower() not in STOPWORDS])

# Function to group common terms
def group_terms(text, group_input):
    try:
        # Regular expression to extract terms and replacement
        match = re.match(r'GROUP=\((.*?)\) TO="(.+?)"', group_input)
        if not match:
            raise ValueError("Invalid input format")

        group_terms = match.group(1).split(',')
        to_term = match.group(2)

        # Cleaning up terms
        group_terms = [term.strip().strip('"') for term in group_terms]

        # Replacing group terms with to_term
        for term in group_terms:
            text = text.replace(term, to_term)
    except Exception as e:
        st.error(f"Error in grouping syntax: {e}")
        return text

    return text

# Initialize session state
if 'color_profile' not in st.session_state:
    st.session_state['color_profile'] = 'Black text, white background'

# Main interface
st.title('Word Cloud Generator')

# Sidebar options
color_profile = st.sidebar.selectbox('Choose Color Profile', 
    ['Black text, white background', 'White text, black background', 
    'Multi-colour text, white background', 'Multi-colour text, black background'], 
    index=0)
st.session_state['color_profile'] = color_profile

max_words = st.sidebar.slider('Maximum Words', 5, 100, 50, 5)

# Upload CSV or text input
uploaded_file = st.file_uploader("Upload a CSV or a text file", type=['csv', 'txt'])
text_input = st.text_area("Or paste your text here")

text = ""
if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        text = ' '.join(df.iloc[:, 0].dropna().astype(str))
    else:
        text = str(uploaded_file.read(), 'utf-8')
elif text_input:
    text = text_input

# Additional stopwords
additional_stopwords = st.text_input('Additional stopwords (separated by commas)', '').split(',')

# Group common terms
group_input = st.text_input('Group common terms (e.g., GROUP=("term1", "term2") TO="new_term")', '')
groupings = {}
if group_input:
    try:
        exec(group_input, {}, groupings)
    except Exception as e:
        st.error(f"Error in grouping syntax: {e}")

# Generating word cloud
if st.button('Generate Word Cloud'):
    if text:
        processed_text = process_text(text, additional_stopwords)
        if group_input:
            processed_text = group_terms(processed_text, group_input)

        # Setting the background color based on the color profile
        bg_color = 'white' if 'white' in color_profile else 'black'

        wordcloud = WordCloud(width=800, height=400, max_font_size=75, max_words=max_words, background_color=bg_color, prefer_horizontal=1, color_func=color_func).generate(processed_text)
        
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.warning('Please upload a file or paste text to generate a word cloud.')
