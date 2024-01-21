import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd
from io import StringIO
import base64

# Function to process text and create a word cloud
def process_text(file_buffer=None, manual_text_input=None):
    # If a file is uploaded, process the file
    if file_buffer is not None:
        text = file_buffer.read().decode('utf-8')
    else:
        text = manual_text_input

    # Remove stopwords
    stopwords = set(STOPWORDS)
    additional_stopwords = st.sidebar.text_area("Add stopwords", "Enter,words,here").split(',')
    stopwords.update(additional_stopwords)

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=200, stopwords=stopwords, collocations=False).generate(text)
    return wordcloud

# Function to handle grouping of common terms
def group_terms(wordcloud, groupings):
    for group in groupings:
        target = group['TO']
        for term in group['GROUP']:
            wordcloud = wordcloud.rec_from_frequencies({target: wordcloud.words_.get(term, 0) + wordcloud.words_.get(target, 0)})
            wordcloud.words_.pop(term, None)
    return wordcloud

# Function to display the word cloud
def display_wordcloud(wordcloud):
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Main app
def main():
    st.title('Word Cloud Generator')
    
    # Sidebar options
    st.sidebar.title("Settings")

    # Text input for manual data entry
    text_input = st.text_area("Paste text data here:")

    # File uploader for CSV or TXT files
    file_buffer = st.file_uploader("Or upload a CSV or TXT file:", type=['csv', 'txt'])

    # Add a button to generate word cloud
    if st.button("Generate Word Cloud"):
        # Process text input or file upload
        wordcloud = process_text(file_buffer, text_input)

        # Group common terms if specified
        groupings_str = st.sidebar.text_area("Group common terms", "GROUP=(\"term1\", \"term2\") TO=\"new_term\"")
        if groupings_str:
            groupings = eval('[' + groupings_str + ']')  # This is a simple method; in production, use a safer parsing method
            wordcloud = group_terms(wordcloud, groupings)

        # Display the generated word cloud
        display_wordcloud(wordcloud)

if __name__ == "__main__":
    main()
