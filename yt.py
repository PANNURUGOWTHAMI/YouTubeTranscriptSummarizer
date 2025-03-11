import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from IPython.display import YouTubeVideo
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

st.markdown("<p style='font-size: 50px; text-align: center; color: red; '>YouTube Transcript Summarizer</p>", unsafe_allow_html=True)


# Streamlit app title
# st.title("YouTube Video Summarizer")

# Input field for the YouTube video link
video = st.text_input("Enter YouTube Video Link:")
start_min = st.number_input("Enter Start Time - Minutes:", step=1)
start_sec = st.number_input("Enter Start Time - Seconds:", step=1)
percent = st.number_input("How much percentage of summary you want? ", step=10)
# Calculate start time in seconds
start_time = start_min * 60 + start_sec

# Check if the link is provided
if video:
    # Button to trigger the summary generation
    if st.button("Generate Transcript"):
        try:
            id_video = video.split("=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(id_video)
            doc = ""
            for line in transcript:
                if line["start"] >= start_time:
                    doc = doc + " " + line["text"]
            doc = []
            for line in transcript:
                if line["start"] >= start_time:
                    if "\n" in line["text"]:
                        x = line["text"].replace("\n", " ")
                        doc.append(x)
                    else:
                        doc.append(line["text"])
            paragraph = " ".join(doc)
            st.subheader("Generated Transcript:")
            st.markdown(
                f"<p style='text-align: justify;'> {paragraph} </p>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    if st.button("Generate Summary"):
        try:
            id_video = video.split("=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(id_video)
            doc = ""
            for line in transcript:
                if line["start"] >= start_time:
                    doc = doc + " " + line["text"]
            doc = []
            for line in transcript:
                if line["start"] >= start_time:
                    if "\n" in line["text"]:
                        x = line["text"].replace("\n", " ")
                        doc.append(x)
                    else:
                        doc.append(line["text"])
            paragraph = " ".join(doc)
            stopwords = list(STOP_WORDS)
            punctuation = punctuation + "\n"
            text = paragraph
            space = spacy.load("en_core_web_sm")
            doc = space(text)
            word_frequencies = {}
            for word in doc:
                if word.text.lower() not in stopwords:
                    if word.text.lower() not in punctuation:
                        if word.text not in word_frequencies.keys():
                            word_frequencies[word.text] = 1
                        else:
                            word_frequencies[word.text] += 1
            max_frequency = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = word_frequencies[word] / max_frequency
            sentence_tokens = [sent for sent in doc.sents]
            sentence_scores = {}
            for sent in sentence_tokens:
                for word in sent:
                    if word.text.lower() in word_frequencies.keys():
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]
            ratio = (int(percent)) / 100
            select_length = int(len(sentence_tokens) * ratio)
            if select_length == 0:
                select_length = 1
            summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
            final_summary = [word.text for word in summary]
            summary_bullets = "\n".join([f"- {sent}" for sent in final_summary])
            st.subheader("Generated Summary:")
            # video_title = transcript[0]['text']
            # st.write(video_title)
            st.markdown(
                f"<ul style='text-align: justify;'>{'<li>'.join(final_summary)}</ul>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
