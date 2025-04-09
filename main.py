import torch
import os

from utils.preprocessing import load_friends_scripts, split_documents
from utils.vectorstore import create_local_embeddings, save_faiss_index

def get_device():
    """
    Returns the best available device: CUDA, MPS (Mac), or CPU.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")  # for Mac with Apple Silicon
    else:
        return torch.device("cpu")

def main():
    device = get_device()
    print(f"🚀 Using device: {device}")

    data_path = "data/scripts_friends"
    docs = load_friends_scripts(data_path)
    print(f"📚 Episodes loaded: {len(docs)}")

    split_docs = split_documents(docs)
    print(f"🧩 Chunks after splitting: {len(split_docs)}")
    # print sample chunk and metadata
    #print("🔍 Sample chunk:\n", split_docs[0].page_content[:300])
    #print("📝 Metadata:\n", split_docs[0].metadata)
    # Crear embeddings y FAISS index
    embeddings = create_local_embeddings()
    os.makedirs("vectorstore", exist_ok=True)
    save_faiss_index(split_docs, embeddings)

if __name__ == "__main__":
    main()
