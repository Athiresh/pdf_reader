# Application using streamlit
import streamlit as st
import pytesseract
import os
from PIL import Image
from pdf2image import convert_from_bytes
from gtts import gTTS
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("PDF Text Extractor, Reader, and Translator")

uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])

if uploaded_file is not None:

    st.text("PDF file successfully uploaded!")
    st.write("Extracting text...")

    # Save the uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    pages = []

    try:
        images = convert_from_bytes(open("temp.pdf", "rb").read())

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            pages.append(text)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

    extracted_text = "\n".join(pages)
    st.subheader("Extracted Text:")
    st.text_area("Text", extracted_text, height=300)

    # Generate audio from the extracted text (in original language)
    speech_original = gTTS(text=extracted_text, lang='en')
    audio_original_filename = os.path.splitext(uploaded_file.name)[0] + '_audio_original.mp3'
    speech_original.save(audio_original_filename)
    st.audio(audio_original_filename, format='audio/mp3', start_time=0)

    # Check if the original text extraction is successful before allowing translation and translated audio playback
    if extracted_text:
        st.write("Text extraction successful!")
        target_language = st.text_input("Enter Target Language Code for translation (e.g., 'hi' for Hindi, 'fr' for French, 'es' for Spanish, 'de' for German, 'it' for Italian)")

        # Provide translation option
        if target_language:
            st.text("Translating text...")
            translator = Translator()
            translated_text = translator.translate(extracted_text, src='en', dest=target_language).text
            st.subheader("Translated Text:")
            st.text_area("Translated Text", translated_text, height=300)

            # Generate audio from the translated text
            speech_translated = gTTS(text=translated_text, lang=target_language)
            audio_translated_filename = os.path.splitext(uploaded_file.name)[0] + '_audio_' + target_language + '.mp3'
            speech_translated.save(audio_translated_filename)
            st.audio(audio_translated_filename, format='audio/mp3', start_time=0)

            st.success("Text translated and translated audio generated successfully!")

    # Remove the temporary file after processing
    os.remove("temp.pdf")