from bert_score import score
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from helpers.LLM_prompts import LLMs_system_prompts
from helpers.hacer_inferencia import get_LLM_response

# Load SBERT model 
_sbert = SentenceTransformer('all-MiniLM-L6-v2')

def answer_chunks_metrics(respuesta_LLM, similar_chunks):
    # 1) Get chunk texts
    chunk_texts = [chunk[3] for chunk, _ in similar_chunks]  # chunk = (doc_id, name, num, text)

    # 2) Prepare list for BERTScore
    candidates = [respuesta_LLM]
    references = [chunk_texts]

    # 3) Calculate BERTScore
    P, *_ = score(
        candidates,
        references,
        lang="en",
        model_type="bert-base-uncased",
        rescale_with_baseline=True
    )

    p = P.mean().item()

    # 4) Print precision results 
    print(f"Precision: {p:.4f}")

    # 5) Calculate SBERT cosine similarity between LLM response and chunks
    chunks_text = " ".join(chunk_texts)  # Combine all chunk texts into one string
    resp_emb = _sbert.encode(respuesta_LLM, normalize_embeddings=True)
    chunks_emb = _sbert.encode(chunks_text, normalize_embeddings=True)
    cosine = float(np.dot(resp_emb, chunks_emb))

    print(f"Response-Chunks Cosine Similarity: {cosine:.4f}")

    return p, cosine

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
