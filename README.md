This is a Streamlit-based language translation app that uses Groq's Mixtral-8x7B-32768 model for translating text between multiple languages. The app also includes language detection, synonym suggestion, word count, and translation history tracking.

Features
✅ Translate text between English, French, German, Spanish, and Italian
✅ Auto-detect input language (if selected)
✅ Show synonyms for the first translated word
✅ Validate text length and warn if it's too long
✅ Track translation history
✅ Clear history and reset the app


Installation & Setup
1️⃣ Clone the Repository
2️⃣ Install Dependencies
pip install streamlit langchain_groq langdetect nltk
3️⃣ Set Up Groq API Key
Create a file named secret_key.py in the project directory and add your API key:
groqapi_key = "your_groq_api_key_here"
4️⃣ Run the App
streamlit run app.py(replace app.py with transulator.py/transulator1.py)



Dependencies
Streamlit → UI framework
Langchain & Groq → LLM integration
Langdetect → Language detection
NLTK (wordnet) → Synonym generation


Usage
1️⃣ Select the input and output language
2️⃣ Enter the text to translate
3️⃣ Click "Translate" to get results
4️⃣ View synonyms, word count, and history
5️⃣ Clear history anytime


🚀 Happy Translating! 😃
