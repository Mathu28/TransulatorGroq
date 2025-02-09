import os
from secret_key import groqapi_key
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langdetect import detect
import nltk
from nltk.corpus import wordnet

# Download wordnet for synonym suggestion
nltk.download('wordnet')

# Set the Groq API key as an environment variable
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = groqapi_key

# Create an instance of ChatGroq
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Streamlit app UI
st.title("Language Translation with Groq")

# Input fields for translation
input_language = st.selectbox("Select the input language", ["English", "French", "German", "Spanish", "Italian", "Auto Detect"])
output_language = st.selectbox("Select the output language", ["English", "French", "German", "Spanish", "Italian"])
input_text = st.text_area("Enter text to translate")

# History of translations
if "history" not in st.session_state:
    st.session_state.history = []

# Function to detect language and return full language name
def detect_language(text):
    try:
        language = detect(text)
        # Mapping language code to full language name
        language_map = {
            "en": "English",
            "fr": "French",
            "de": "German",
            "es": "Spanish",
            "it": "Italian",
            "nl": "Dutch",
        }
        return language_map.get(language, language)  # Default to language code if not in map
    except Exception as e:
        return str(e)

# Function to get synonyms of a word
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

# Function to check text length
def validate_text_length(text):
    max_length = 500
    if len(text) > max_length:
        st.warning(f"Your input text is too long! It has {len(text)} characters. Consider shortening it.")
    else:
        st.success(f"Text length is acceptable: {len(text)} characters.")

# Button to process translation
if st.button("Translate"):
    if input_text:
        if input_language == "Auto Detect":
            detected_language = detect_language(input_text)
            st.write(f"Detected language: {detected_language}")

        # Translate the text using Groq model
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant that translates {input_language} to {output_language}.",
                ),
                ("human", "{input}"),
            ]
        )

        # Chain the prompt with the LLM
        chain = prompt | llm

        # Invoke the chain with dynamic values for language and text
        response = chain.invoke(
            {
                "input_language": input_language,
                "output_language": output_language,
                "input": input_text,
            }
        )

        # Display the result
        st.subheader(f"Translation from {input_language} to {output_language}")
        st.write(response.content)

        # Show synonyms of the translated word (if any)
        if response.content:
            words = response.content.split()
            synonyms = get_synonyms(words[0])  # Taking the first word for simplicity
            if synonyms:
                st.write(f"Synonyms for '{words[0]}': {', '.join(synonyms)}")

        # Validate text length
        validate_text_length(input_text)

        # Word count for input text
        input_word_count = len(input_text.split())
        st.write(f"Word count of input text: {input_word_count}")

        # Save translation history
        st.session_state.history.append({
            "input_language": input_language,
            "output_language": output_language,
            "input_text": input_text,
            "output_text": response.content
        })

    else:
        st.error("Please enter some text to translate.")

# Display translation history
if st.session_state.history:
    st.subheader("Translation History")
    for item in st.session_state.history:
        st.write(f"**{item['input_language']} to {item['output_language']}**")
        st.write(f"Input: {item['input_text']}")
        st.write(f"Output: {item['output_text']}")
        st.text("---")

# Option to clear text input and history
if st.button("Clear History"):
    st.session_state.history = []  # Option to clear history as well
    st.rerun()  # Refresh the app
