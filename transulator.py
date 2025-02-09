import os
from secret_key import groqapi_key
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

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
input_language = st.selectbox("Select the input language", ["English", "French", "German", "Spanish", "Italian"])
output_language = st.selectbox("Select the output language", ["English", "French", "German", "Spanish", "Italian"])
input_text = st.text_area("Enter text to translate")

# Button to process translation
if st.button("Translate"):
    if input_text:
        # Translation prompt template
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
    else:
        st.error("Please enter some text to translate.")


