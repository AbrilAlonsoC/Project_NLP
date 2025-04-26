# Friends TV Show Chatbot (RAG System)

A lightweight multilingual Retrieval-Augmented Generation (RAG) chatbot based on the TV show Friends.  
It answers user questions by retrieving relevant script chunks and generating grounded, contextualized responses.

---

## 📚 Project Overview

- **Multilingual support**: Input in English, Spanish, French, German, Portuguese, Italian, or Chinese.
- **Translation Layer**: Automatic translation (via MarianMT) to English for processing, then back to the input language.
- **Document database**: 234 scripts from all episodes of Friends, processed into individual Markdown files.
- **Retrieval-augmented**: Semantic search over embeddings to find relevant content before generation.
- **LLM**: meta-llama/llama-4-scout:free via OpenRouter API.
- **Frontend**: Streamlit-based chat interface with styled chat bubbles and persistent history.

---

## 🛠️ Technologies Used

- `transformers` (MarianMT models for translation)
- `sentence-transformers` (distiluse-base-multilingual-cased-v2 for embeddings)
- `bert-score` and `SBERT` (evaluation metrics)
- `streamlit` (frontend interface)
- `litellm` (LLM API interaction via OpenRouter)
- `langdetect` (language detection)

---

## 🗂️ Repository Structure
```
root/
├── conversor.py                 # Convert TXT scripts to Markdown.
├── crear_indice.py              # Build the vector index (chunks + embeddings).
├── inferencia_interfaz.py       # Backend to handle question answering logic.
├── interfaz.py                  # Streamlit web app interface for the chatbot.
├── helpers/                     # Folder containing all helper modules.
│   ├── crear_indice.py          # Functions for chunking documents and creating embeddings.
│   ├── hacer_inferencia.py      # Retrieval and LLM inference functions.
│   ├── metrics.py               # Evaluation metrics (BERTScore, SBERT Cosine, Exact Match Rate).
│   ├── LLM_prompts.py           # Custom system prompt for controlled LLM behavior.
│   └── translation.py           # Language detection and translation using MarianMT models.
├── data/                        # Folder with the script datasets.
│   ├── scripts_friends/         # Original Friends TV show scripts in TXT format.
│   └── scripts_friends_md/      # Converted scripts in Markdown format.
├── Indice/                      # Folder where chunks and embeddings are saved.
├── Interfaz-Images/             # Background images for the Streamlit app.
├── .env                         # Environment file storing OpenRouter API key (not pushed to GitHub).
└── requirements.txt             # Python dependencies required for the project.
```

---
## 🔑 OpenRouter API Key Setup

An example `.env` file is already included in the repository.  
It looks like this:

```ini
# Replace this API key with your own OpenRouter key to avoid hitting shared usage limits (200 requests per user).
You can register and obtain a free API key here: https://openrouter.ai/.
This ensures that you have your own usage quota and are not limited by a shared key.
LLMsAPIkey_v7 = "your_openrouter_api_key_here"

```
---

## ⚙️ How to Run

1. Install requirements:

```
pip install -r requirements.txt
```
2. Create a `.env` file in the root directory:

LLMsAPIkey_v7=your_openrouter_api_key_here


3. Build the index:
```
python index.py
````
4. Launch the chatbot interface:
```
streamlit run interfaz.py
````
## 🔎 Evaluation metrics 

* BERTScore: Measures alignment between generated responses and retrieved content.
* SBERT Cosine Similarity: Measures semantic relevance between the question and the generated response.
* Exact Match Rate: Evaluates presence of expected keywords in answers.
