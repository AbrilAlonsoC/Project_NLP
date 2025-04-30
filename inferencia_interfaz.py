from helpers.translation import detect_language, translate_to_english, translate_to_original
import os
from dotenv import load_dotenv
from helpers.crear_indice import load_data
from helpers.hacer_inferencia import get_similar_chunks
from helpers.LLM_prompts import LLMs_system_prompts
from helpers.hacer_inferencia import get_LLM_response
from helpers.metrics import answer_chunks_metrics, answer_question_metrics
import requests
import warnings
import time

warnings.filterwarnings("ignore")

# Desactivate SSL verification 
old_init = requests.Session.__init__
def new_init(self):
    old_init(self)
    self.verify = False
requests.Session.__init__ = new_init

load_dotenv()

def responder_pregunta(question):
    ###### Parameters
    top_n = 10
    ######

    # Start the timer
    start_time = time.time()

    # Detect the original language
    detected_lang = detect_language(question)
    
    # Translate to English if the detected language is not English
    if detected_lang != "en":
        question_en = translate_to_english(question, detected_lang)
    else:
        question_en = question

    # Answer the question using the LLM
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    save_folder = os.path.join(script_dir, 'Indice')

    chunks, embeddings, model = load_data(save_folder)
    similar_chunks = get_similar_chunks(question_en, chunks, embeddings, model, top_n)

    user_prompt = f"Question: {question_en}\n\nConocimiento:\n"
    for i, (chunk, similarity) in enumerate(similar_chunks, 1):
        doc_id, doc_name, chunk_number, chunk_text = chunk
        user_prompt += f"{doc_name}: {chunk_text}\n"

    APIkey_OpenRouter = os.getenv("LLMsAPIkey_v7")
    system_prompt = LLMs_system_prompts("elaborate_responses", "", "")
    respuesta_LLM_en = get_LLM_response(
        "OpenRouter",
        APIkey_OpenRouter,
        "meta-llama/llama-4-scout:free",
        user_prompt,
        system_prompt
    )

    # Translate the LLM response back to the original language if it was translated
    if detected_lang != "en":
        respuesta_LLM = translate_to_original(respuesta_LLM_en, detected_lang)
    else:
        respuesta_LLM = respuesta_LLM_en

    # Evluate chunks (content) versus LLM response 
    p, cos_ca = answer_chunks_metrics(respuesta_LLM, similar_chunks)

    # Evluate if the answer actually responses to the question: question versus LLM response 
    cos_qa = answer_question_metrics(question, respuesta_LLM)

    # End timer
    end_time = time.time()

    # Print time response
    print(f"Time response: {end_time - start_time:.2f} seconds")

    return respuesta_LLM, similar_chunks, p, cos_ca, cos_qa


