from transformers import pipeline

_translator = None

def get_translator():
    """
    Lazily load and return a multilingual→English translation pipeline.
    """
    global _translator
    if _translator is not None:
        return _translator
    model_name = "Helsinki-NLP/opus-mt-mul-en"
    _translator = pipeline("translation", model=model_name)
    return _translator

def translate_to_english(text):
    """
    Translate a single text to English. Returns the translated string.
    If text is empty, returns the original text.
    """
    if not text or not text.strip():
        return text
    translator = get_translator()
    try:
        return translator(text)[0]['translation_text']
    except Exception:
        return text

def translate_indian_languages():
    """
    Loads a highly reliable multilingual model to translate text from various
    languages into English.
    """
    # This model is from the Helsinki-NLP group, the standard for translation tasks.
    # It handles multiple source languages automatically without needing special tags.
    print(f"Loading translation model for demo...")
    try:
        translator = get_translator()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load the model. Please check your internet connection and library installation. Error: {e}")
        return

    # --- Prepare a list of example sentences to translate ---
    sentences_to_translate = [
        "चेतावनी! चक्रवात तट के करीब आ रहा है, तुरंत खाली करें!", # Hindi
        "আজ আবহাওয়া খুব মনোরম।", # Bengali
        "మీరు ఎలా ఉన్నారు?", # Telugu
        "The meeting is scheduled for 3 PM tomorrow.", # English (will be handled gracefully)
    ]

    print("\n--- Translating Sentences ---")

    for sentence in sentences_to_translate:
        try:
            # --- SIMPLIFIED: No language detection needed ---
            # This model automatically handles different source languages.
            translated_text = translator(sentence)[0]['translation_text']
            
            print(f"Original: '{sentence}'")
            print(f"Translated: '{translated_text}'")
            print("-" * 25)
            
        except Exception as e:
            print(f"Could not process sentence: '{sentence}'. Error: {e}")

if __name__ == "__main__":
    translate_indian_languages()

