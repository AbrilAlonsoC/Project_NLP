import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def create_local_embeddings(model_name="all-MiniLM-L6-v2"):
    """
    Loads a local embedding model from HuggingFace.
    """
    return HuggingFaceEmbeddings(model_name=model_name)

def save_faiss_index(documents, embedding_model, index_path="vectorstore/faiss_index"):
    """
    Creates and saves a FAISS index from the given documents.
    """
    db = FAISS.from_documents(documents, embedding_model)
    db.save_local(index_path)
    print(f"✅ FAISS index saved at {index_path}")

def load_faiss_index(embedding_model, index_path="vectorstore/faiss_index"):
    """
    Loads an existing FAISS index from local storage.
    """
    return FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
