from bert_score import score
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from helpers.LLM_prompts import LLMs_system_prompts
from helpers.hacer_inferencia import get_LLM_response

# helpers/metrics.py

def answer_chunks_metrics(respuesta_LLM, similar_chunks):
    # 1) Extrae solo los textos de los chunks
    chunk_texts = [chunk[3] for chunk, _ in similar_chunks]  # chunk = (doc_id, name, num, text)

    # 2) Prepara listas para BERTScore
    candidates = [respuesta_LLM]
    references = [chunk_texts]

    # 3) Llama a score
    P, R, F1 = score(
        candidates,
        references,
        lang="en",
        model_type="bert-base-uncased",
        rescale_with_baseline=True
    )

    p = P.mean().item()
    r = R.mean().item()
    f = F1.mean().item()

    # Imprime en consola 
    print(f"Precision: {p:.4f}")
    print(f"Recall:    {r:.4f}")
    print(f"F1:        {f:.4f}")

    return p, r, f



# carga un modelo SBERT (solo una vez)
_sbert = SentenceTransformer('all-MiniLM-L6-v2')

def answer_question_metrics(question: str, answer: str):
    q_emb = _sbert.encode(question, normalize_embeddings=True)
    a_emb = _sbert.encode(answer, normalize_embeddings=True)
    cosine = float(np.dot(q_emb, a_emb))
    print(f"Relevance (SBERT cosine) = {cosine:.4f}")
    return cosine

__all__ = [
    "answer_chunks_metrics_compact",
    "answer_question_metrics",
    "exact_match_rate"
]
