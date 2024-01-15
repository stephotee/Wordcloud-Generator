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
            df = pd.read_csv(uploaded_file)
            text = ' '.join(row[0] for row in df.values)
        else:
            text = str(uploaded_file.read(), 'utf-8')

        processed_text = process_text(text)

    elif text_input:
        processed_text = process_text(text_input)

    if processed_text:
        wordcloud = WordCloud(width=800, height=400, max_font_size=75, max_words=50, font_path=font_path(), color_func=lambda *args, **kwargs: 'black').generate(processed_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        # Convert plot to PNG image
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        st.markdown(get_image_download_link(Image.open(img_buf), 'wordcloud.png', 'Download Word Cloud as PNG'), unsafe_allow_html=True)

# Restart button
if st.button("Create another word cloud"):
    st.experimental_rerun()
