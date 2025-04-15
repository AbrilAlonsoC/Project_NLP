import os
from dotenv import load_dotenv
from helpers.crear_indice import load_data
from helpers.hacer_inferencia import get_similar_chunks
from helpers.LLM_prompts import LLMs_system_prompts
from helpers.hacer_inferencia import get_LLM_response
import requests

# Desactiva la verificación SSL
old_init = requests.Session.__init__
def new_init(self):
    old_init(self)
    self.verify = False
requests.Session.__init__ = new_init

load_dotenv()

def responder_pregunta(question):
    ###### Parámetros
    top_n = 3
    ######

    # Parte 2: Responder preguntas
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Path de este script
    save_folder = os.path.join(script_dir, 'Indice')

    # Cargar los datos procesados
    chunks, embeddings, model = load_data(save_folder)

    # Obtener los chunks más similares
    similar_chunks = get_similar_chunks(question, chunks, embeddings, model, top_n)

    # Construir el prompt
    user_prompt = f"Question: {question}\n\nConocimiento:\n"
    print("Los chunks más similares a tu pregunta son:\n")
    for i, (chunk, similarity) in enumerate(similar_chunks, 1):
        doc_id, doc_name, chunk_number, chunk_text = chunk
        print(f"{i}. DOCID: {doc_id} | Document Name: {doc_name} | Chunk number: {chunk_number} | Similarity: {similarity:.4f}\n{chunk_text}\n")
        user_prompt += f"{doc_name}: {chunk_text}\n"

    # Obtener respuesta del modelo
    APIkey_OpenRouter = os.getenv("LLMsAPIkey_v7")
    system_prompt = LLMs_system_prompts("elaborate_responses", "", "")
    respuesta_LLM = get_LLM_response(
        "OpenRouter",
        APIkey_OpenRouter,
        "meta-llama/llama-4-scout:free",
        user_prompt,
        system_prompt
    )

    print(respuesta_LLM)
    return respuesta_LLM
