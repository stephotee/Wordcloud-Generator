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

# Function to apply custom grouping
def apply_custom_grouping(text, groupings):
    for group_words, to_word in groupings.items():
        for word in group_words:
            text = text.replace(word, to_word)
    return text

# Initialize session state
if 'color_profile' not in st.session_state:
    st.session_state['color_profile'] = 'Black text, white background'

# Main interface
st.title('Word Cloud Generator')

# Sidebar options
additional_stopwords = st.sidebar.text_input("Additional stopwords (comma separated)")

grouping_counter = 1
groupings = []
# Custom word grouping
if st.sidebar.button("Custom word grouping"):
    grouping_counter += 1
for _ in range(grouping_counter):
    with st.sidebar:
        group = st.text_input(f"Words to be grouped (Group {_})", "")
        new_term = st.text_input(f"New term for group (To {_})", "")
        if group and new_term:
            groupings.append((group.split(','), new_term))

additional_stopwords = st.sidebar.text_input("Additional stopwords (comma separated)")

max_words = st.sidebar.slider("Max words", 5, 100, 5, step=5)

# Custom word grouping interface
groupings = {}
if st.sidebar.button('Custom word grouping'):
    group_num = len(groupings) + 1
    group_words = st.sidebar.text_input(f"Words to be grouped {group_num}", key=f"group{group_num}")
    to_word = st.sidebar.text_input(f"Replacement word {group_num}", key=f"to{group_num}")
    if group_words and to_word:
        groupings[group_words.split(',')] = to_word

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

# Generate button
if st.button('Generate Word Cloud'):
    if text:
        processed_text = process_text(text, additional_stopwords)
        processed_text = apply_custom_grouping(processed_text, groupings)

        # Setting the background color based on the color profile
        bg_color = 'white' if 'white' in color_profile else 'black'

        wordcloud = WordCloud(width=800, height=400, max_font_size=75, max_words=max_words, background_color=bg_color, prefer_horizontal=1, color_func=color_func).generate(processed_text)
        
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.warning('Please upload a file or paste text to generate a word cloud.')
