import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from io import BytesIO
import base64

# Function to generate word cloud
def generate_wordcloud(data, additional_stopwords, group_terms_mapping, color_scheme, max_words):
    stopwords = set(STOPWORDS)
    stopwords.update(additional_stopwords)
    
    # If grouping terms are provided, we process them here
    if group_terms_mapping:
        for term, group in group_terms_mapping.items():
            data = data.replace(term, group)
    
    wordcloud = WordCloud(stopwords=stopwords,
                          prefer_horizontal=1.0,
                          width=800,
                          height=400,
                          background_color=color_scheme['background_color'],
                          color_func=lambda *args, **kwargs: color_scheme['text_color'],
                          max_words=max_words).generate(data)

    return wordcloud

# Function to decode the image and make it downloadable
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Function to parse the group terms from the user input
def parse_group_terms(group_terms_str):
    groups = group_terms_str.split('TO="')
    group_terms_mapping = {}
    for group in groups[1:]:
        terms, group_name = group.split('")')
        terms = terms.strip('GROUP=("').split('", "')
        group_name = group_name.strip()
        for term in terms:
            group_terms_mapping[term] = group_name
    return group_terms_mapping

# UI for the app
st.title("Word Cloud Generator")
st.sidebar.title("Settings")

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    text_column = st.sidebar.selectbox("Which column contains the text data?", data.columns)
    data = data[text_column].dropna().astype(str)

# UI to add additional stopwords
additional_stopwords = st.sidebar.text_area("Add stop words separated by commas", "").split(',')

# UI to group common terms
group_terms_str = st.sidebar.text_area('Group common terms', 'GROUP=("term1", "term2") TO="group_name"')

# UI for color scheme selection
color_scheme_option = st.sidebar.radio(
    "Select Color Scheme",
    ('Black text, white background', 'White text, black background', 'Multi-color text, white background', 'Multi-color text, black background')
)

# Mapping color schemes to their respective settings
color_schemes = {
    'Black text, white background': {'text_color': '#000000', 'background_color': '#FFFFFF'},
    'White text, black background': {'text_color': '#FFFFFF', 'background_color': '#000000'},
    'Multi-color text, white background': {'text_color': None, 'background_color': '#FFFFFF'},
    'Multi-color text, black background': {'text_color': None, 'background_color': '#000000'}
}

# Selecting the appropriate color scheme
color_scheme = color_schemes[color_scheme_option]

# UI for maximum words in the word cloud
max_words = st.sidebar.slider("Max number of words", 5, 100, 5, 5)

if st.button("Generate Word Cloud"):
    group_terms_mapping = parse_group_terms(group_terms_str)
    wordcloud = generate_wordcloud(' '.join(data), additional_stopwords, group_terms_mapping, color_scheme, max_words)
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    st.pyplot()
    
    # Show download link
    img = wordcloud.to_image()
    st.markdown(get_image_download_link(img, "wordcloud.png", 'Download Wordcloud'), unsafe_allow_html=True)
