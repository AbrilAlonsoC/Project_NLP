import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from utils.vectorstore import create_local_embeddings, load_faiss_index

def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

def load_local_llm(model_name="google/flan-t5-base"):
    print("🔁 Loading local LLM...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

def generate_answer(context, question, tokenizer, model, device):
    #  Zero-Shot Prompting: context + question
    # prompt = f"Answer the question based on the context below.\n\nContext:\n{context}\n\nQuestion: {question}"
    # Zero-Shot Prompting + Instruction Prompting
    # Prompting type: Zero-Shot + Instruction Prompting
    prompt = f"""
    Answer the user's question using only the context provided. 
    If the answer is not in the context, say "I don't know". 
    Do not hallucinate.

    Context:
    {context}

    Question: {question}

    Answer:
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(device)
    output = model.generate(**inputs, max_new_tokens=150)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

def main():
    device = get_device()
    print(f"🚀 Using device: {device}")

    # Paso 1: cargar embeddings y FAISS index
    embeddings = create_local_embeddings()
    vector_db = load_faiss_index(embeddings)

    # Paso 2: hacer una query
    question = input("❓ Escribe tu pregunta: ")
    top_k = 10
    docs = vector_db.similarity_search(question, k=top_k)

    # Paso 3: concatenar el contexto de los docs encontrados
    context = "\n\n".join(doc.page_content for doc in docs)

    # Paso 4: cargar modelo local
    tokenizer, model = load_local_llm()
    model.to(device)

    # Paso 5: generar respuesta
    # Mostrar qué episodios están en el contexto
    episodes = set()
    for doc in docs:
        season = doc.metadata.get("season")
        episode = doc.metadata.get("episode")
        episodes.add(f"Season {season}, Episode {episode}")

    # Generar respuesta
    answer = generate_answer(context, question, tokenizer, model, device)

    # Mostrar resultado
    print("\n📌 Respuesta generada:")
    print(answer)
    print("\n📍 Basado en los episodios:")
    print("\n".join(sorted(episodes)))




if __name__ == "__main__":
    main()
