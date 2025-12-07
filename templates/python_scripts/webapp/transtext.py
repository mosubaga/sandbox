import streamlit as st
from transformers import MarianMTModel, MarianTokenizer

def translate_text(segment, lang):
    langpairs = {
        "fr": "Helsinki-NLP/opus-mt-en-fr",
        "de": "Helsinki-NLP/opus-mt-en-de",
        "es": "Helsinki-NLP/opus-mt-en-es",
        "zh": "Helsinki-NLP/opus-mt-en-zh",
        "jp": "Helsinki-NLP/opus-mt-en-jap"
    }

    # Load model and tokenizer
    model_name = langpairs[lang]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    inputs = tokenizer(segment, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

# Streamlit UI
st.title("Translate text")

text_input = st.text_input("Source text:", key="text_input")

language_options = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Simplified Chinese": "zh",
    "Japanese": "jp"
}

selected_lang = st.selectbox(
    "Target language:",
    options=list(language_options.keys()),
    index=0
)

if st.button("Translate"):
    if text_input:
        try:
            with st.spinner("Translating..."):
                translated = translate_text(text_input, language_options[selected_lang])
            st.success(f"**Translation:** {translated}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter text to translate")

