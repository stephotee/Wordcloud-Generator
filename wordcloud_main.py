import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter

# Function to parse the group mapping input from the user
def parse_group_terms(group_terms_str):
    group_regex = r'GROUP=\((.*?)\) TO="(.+?)"'
    groups = re.findall(group_regex, group_terms_str)
    group_mapping = {}
    for group in groups:
        terms = group[0].replace('"', '').split(', ')
        new_term = group[1]
        for term in terms:
            group_mapping[term] = new_term
    return group_mapping

# Function to apply the grouping of terms in the text
def apply_grouping(text, group_mapping):
    word_freq = Counter(text.split())
    for old_term, new_term in group_mapping.items():
        if old_term in word_freq:
            word_freq[new_term] += word_freq.pop(old_term)
    return ' '.join([word for word in text.split() if word not in group_mapping]), word_freq

# Function to generate the word cloud
def generate_wordcloud(text, word_freq, max_words, color_choice):
    wordcloud = WordCloud(width=800, height=400, max_font_size=75,
                          max_words=max_words, background_color='white',
                          color_func=lambda *args, **kwargs: color_choice).generate_from_frequencies(word_freq)
    
    # Display the generated word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

# Streamlit UI
st.title("Word Cloud Generator")
user_input = st.text_area("Paste your text here:")
max_words = st.number_input("Maximum number of words", min_value=1, max_value=100, value=50)
color_choice = st.color_picker("Choose the text color for the word cloud", '#000000')
group_terms_input = st.text_area("Group common terms (e.g., GROUP=(\"battery\", \"long battery\", \"long battery life\") TO=\"battery\")")

# Generate button
if st.button("Generate Word Cloud"):
    group_mapping = parse_group_terms(group_terms_input)
    processed_text, grouped_word_freq = apply_grouping(user_input, group_mapping)
    generate_wordcloud(processed_text, grouped_word_freq, max_words, color_choice)
