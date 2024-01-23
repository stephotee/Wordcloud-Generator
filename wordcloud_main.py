import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import io
from PIL import Image
import nltk
# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')




# Initialize NLTK stop words
nltk_stopwords = stopwords.words('english')

# Function to generate the word cloud
def generate_wordcloud(text_data, additional_stopwords, max_words, color_scheme, text_case):
    # Tokenize words
    tokens = word_tokenize(text_data)
    # Remove punctuation and make lower case
    tokens = [word.lower() for word in tokens if word.isalpha()]
    
    # Apply text case
    if text_case == 'Upper case':
        tokens = [word.upper() for word in tokens]
    elif text_case == 'Lower case':
        tokens = [word.lower() for word in tokens]

    # Add additional stop words if any
    if additional_stopwords:
        additional_stopwords = [word.strip().lower() for word in additional_stopwords.split(',')]
        all_stopwords = nltk_stopwords + additional_stopwords
    else:
        all_stopwords = nltk_stopwords

    # Remove stop words
    tokens = [word for word in tokens if not word in all_stopwords]

    # Generate word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400,
        max_font_size=60, 
        min_font_size=8, 
        max_words=max_words, 
        background_color='white',
        color_func=color_scheme
    ).generate(' '.join(tokens))
    
    return wordcloud

# Function to handle color scheme
def get_color_scheme(text_colour):
    if text_colour == 'Black text':
        return lambda *args, **kwargs: 'black'
    elif text_colour == 'Colourful':
        return lambda *args, **kwargs: "hsl(%d, 100%%, 50%%)" % np.random.randint(0, 360)

# Function to save word cloud to a buffer
def save_wordcloud(wordcloud):
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer

# Streamlit UI layout
st.title('Word Cloud Generator')

# Sidebar controls
st.sidebar.title("Controls")
number_of_words = st.sidebar.slider('Number of words', 5, 100, 50, 5)
text_colour = st.sidebar.selectbox('Text colour', ['Black text', 'Colourful'])
text_case = st.sidebar.selectbox('Text case', ['Upper case', 'Lower case'])
additional_stop_words = st.sidebar.text_area('Additional stop words', '')

# Upload file
uploaded_file = st.file_uploader("Choose a text or CSV file", type=['txt', 'csv'])
if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        text_data = ' '.join(df[df.columns[0]].dropna().astype(str).tolist())
    else:
        text_data = uploaded_file.getvalue().decode("utf-8")
else:
    text_data = st.text_area("Paste text here...")

# Generate and show word cloud
wordcloud_buffer = None  # Initialize buffer for word cloud
if st.button('Generate Word Cloud'):
    color_scheme = get_color_scheme(text_colour)
    wordcloud_obj = generate_wordcloud(text_data, additional_stop_words, number_of_words, color_scheme, text_case)
    wordcloud_buffer = save_wordcloud(wordcloud_obj)  # Save to buffer for download
    plt.imshow(wordcloud_obj, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

# Download button
if wordcloud_buffer and st.button('Download PNG'):
    st.download_button(
        label='Download Word Cloud as PNG',
        data=wordcloud_buffer,
        file_name='wordcloud.png',
        mime='image/png'
    )

# Reset button
if st.button('Start Over'):
    st.experimental_rerun()
