import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

# Function to generate and display word cloud
def generate_wordcloud(text, max_words, color_func):
    wordcloud = WordCloud(stopwords=STOPWORDS, max_words=max_words, background_color='white', 
                          width=800, height=400, random_state=1, 
                          color_func=color_func, normalize_plurals=False).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

# Function to parse the group terms from the user input
def parse_group_terms(group_terms_str):
    groups = group_terms_str.split('TO="')
    group_terms_mapping = {}
    for group in groups[1:]:
        terms, group_name = group.split('")')
        terms = terms.strip('GROUP=("').split('", "')
        group_name = group_name.strip()
        for term in terms:
            group_terms_mapping[term.lower()] = group_name.lower()
    return group_terms_mapping

# Function to download the generated word cloud
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Streamlit UI
st.title("Word Cloud Generator")

# Text input for direct text data
text_data = st.text_area("Paste text data here")

# File uploader for CSV or TXT
uploaded_file = st.file_uploader("...or upload a CSV or TXT file instead", type=['csv', 'txt'])
if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        dataframe = pd.read_csv(uploaded_file)
        text_column = st.selectbox("Which column contains the text data?", dataframe.columns)
        text_data = ' '.join(dataframe[text_column].dropna().astype(str))
    elif uploaded_file.type == "text/plain":
        text_data = str(uploaded_file.read(), 'utf-8')

# Sidebar controls
st.sidebar.header('Word Cloud Settings')
max_words = st.sidebar.slider('Maximum number of words', min_value=5, max_value=100, value=50, step=5)
color_scheme = st.sidebar.radio("Color scheme", ["Black and White", "Colorful"])
additional_stopwords = st.sidebar.text_area("Enter stopwords separated by commas").split(',')

# Group common terms input
group_terms_str = st.sidebar.text_area('Group common terms (syntax: GROUP=("term1", "term2") TO="group_name")')

# Generate button
if st.button('Generate Word Cloud'):
    # Process group terms
    group_terms_mapping = parse_group_terms(group_terms_str)
    
    # Apply grouping of terms
    for original, new in group_terms_mapping.items():
        text_data = text_data.replace(original, new)
    
    # Generate word cloud
    if color_scheme == "Black and White":
        color_func = lambda *args, **kwargs: "black"
    else:
        color_func = None  # Use default color scheme
    
    generate_wordcloud(text_data, max_words, color_func)

    # Display download link
    wordcloud_img = WordCloud().to_image()
    st.markdown(get_image_download_link(wordcloud_img, 'your_wordcloud.png', 'Download Word Cloud'), unsafe_allow_html=True)
