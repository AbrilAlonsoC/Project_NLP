from sentence_transformers import SentenceTransformer
import pickle
import os
import requests
 
old_init = requests.Session.__init__
 
def new_init(self):
    old_init(self)
    self.verify = False
 
requests.Session.__init__ = new_init

# Function to process all Markdown files in a directory
def process_all_markdown_files(carpeta_path, chunk_size, chunk_overlap):
    files = os.listdir(carpeta_path)
    files_array = sorted([file for file in files if os.path.isfile(os.path.join(carpeta_path, file)) 
                          and file.endswith('.md')])
    all_chunks = []

    for file in files_array:
        doc_id = files_array.index(file)
        file_path = os.path.join(carpeta_path, file)
        chunks = process_markdown(file_path, doc_id, file, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)

    return all_chunks


# Function to process Markdown files
def process_markdown(file_path, doc_id, doc_name, chunk_size, chunk_overlap):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Divide the text into chunks
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - chunk_overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append((doc_id, doc_name, i // (chunk_size - chunk_overlap), chunk))

        return chunks
    except Exception as e:
        print(f"Error al procesar el Markdown {doc_name}: {e}")
        return []

# Function to create embeddings
def create_embeddings(chunks, model_embeddings):
    model = SentenceTransformer(model_embeddings)
    embeddings = model.encode([chunk[3] for chunk in chunks])
    return embeddings, model

# Function to save data
def save_data(chunks, embeddings, model, save_folder):
    os.makedirs(save_folder, exist_ok=True)
    with open(os.path.join(save_folder, 'chunks_with_ids.pkl'), 'wb') as f:
        pickle.dump(chunks, f)
    with open(os.path.join(save_folder, 'embeddings.pkl'), 'wb') as f:
        pickle.dump(embeddings, f)
    with open(os.path.join(save_folder, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)

# Function to load data
def load_data(save_folder):
    with open(os.path.join(save_folder, 'chunks_with_ids.pkl'), 'rb') as f:
        chunks = pickle.load(f)
    with open(os.path.join(save_folder, 'embeddings.pkl'), 'rb') as f:
        embeddings = pickle.load(f)
    with open(os.path.join(save_folder, 'model.pkl'), 'rb') as f:
        model = pickle.load(f)
    return chunks, embeddings, model