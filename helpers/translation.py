# helpers/translation.py
from transformers import MarianMTModel, MarianTokenizer

SUPPORTED_LANGUAGES = {
    "es": "Helsinki-NLP/opus-mt-es-en",
    "fr": "Helsinki-NLP/opus-mt-fr-en",
    "de": "Helsinki-NLP/opus-mt-de-en",
    "it": "Helsinki-NLP/opus-mt-it-en",
    "pt": "Helsinki-NLP/opus-mt-ROMANCE-en",
    "zh": "Helsinki-NLP/opus-mt-zh-en",  
}

REVERSE_LANGUAGES = {
    "es": "Helsinki-NLP/opus-mt-en-es",
    "fr": "Helsinki-NLP/opus-mt-en-fr",
    "de": "Helsinki-NLP/opus-mt-en-de",
    "it": "Helsinki-NLP/opus-mt-en-it",
    "pt": "Helsinki-NLP/opus-mt-en-ROMANCE",
    "zh": "Helsinki-NLP/opus-mt-en-zh",  
}



# Function to detect the language of the question
from langdetect import detect

def detect_language(text):
    return detect(text)

# Translate to English
def translate_to_english(text, source_lang):
    if source_lang not in SUPPORTED_LANGUAGES:
        return text   # Return the text as is if not supported
    
    model_name = SUPPORTED_LANGUAGES[source_lang]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return tgt_text

# Translate back to the original language
def translate_to_original(text, target_lang):
    if target_lang not in REVERSE_LANGUAGES:
        return text  # Return the text as is if not supported
    
    model_name = REVERSE_LANGUAGES[target_lang]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return tgt_text
