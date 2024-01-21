import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import io

# Function to parse grouping syntax
def parse_grouping(text):
    groups = {}
    for part in text.split('GROUP=')[1:]:
        group, to = part.split(' TO=')
        group = group.strip("()").replace('"', '').split(', ')
        to = to.split(' ')[0].replace('"', '')
        for word in group:
            groups[word] = to
    return groups

# Update word frequencies based on grouping
def update_frequencies(frequencies, groups):
    new_frequencies = {}
    for word, freq in frequencies.items():
        if word in groups:
            new_frequencies[groups[word]] = new_frequencies.get(groups[word], 0) + freq
        else:
            new_frequencies[word] = freq
    return new_frequencies

def main():
    st.title("Word Cloud Generator")

    # File upload or text input
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            text = ' '.join(df[df.columns[0]])
        else:
            text = uploaded_file.read().decode("utf-8")
    else:
        text = st.text_area("Enter text")

    # Additional stopwords
    new_stopwords = st.text_input("Enter additional stopwords (comma separated)")

    # Grouping common terms
    grouping = st.text_input("Group common terms (syntax: GROUP=(\"term1\", \"term2\") TO=\"new_term\")")

    if st.button("Generate Word Cloud"):
        stopwords = set(STOPWORDS)
        stopwords.update([word.strip() for word in new_stopwords.split(',')])

        wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)
        frequencies = wordcloud.process_text(text)

        if grouping:
            groups = parse_grouping(grouping)
            frequencies = update_frequencies(frequencies, groups)
            wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate_from_frequencies(frequencies)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

if __name__ == "__main__":
    main()
