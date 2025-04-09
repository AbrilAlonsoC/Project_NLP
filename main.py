import torch
from utils.preprocessing import load_friends_scripts, split_documents

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
    print("🔍 Sample chunk:\n", split_docs[0].page_content[:300])
    print("📝 Metadata:\n", split_docs[0].metadata)

if __name__ == "__main__":
    main()
