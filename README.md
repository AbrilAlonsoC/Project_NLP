# Friends TV Show Chatbot (RAG System)

This repository contains a multilingual Retrieval-Augmented Generation (RAG) chatbot based on the TV show Friends. It answers users' questions by retrieving relevant script chunks and generating contextualized responses.

---

## Project Overview

- **Multilingual support**: input in English, Spanish, French, German, Portuguese, Italian, or Chinese
- **Translation Layer**: automatic translation (via MarianMT) to English for processing, then back to the input language
- **Document database**: 234 scripts from all episodes of Friends, processed into individual Markdown files
- **Retrieval-augmented**: semantic search over embeddings to find relevant content before generation based on cosine similarity
- **LLM**: meta-llama/llama-4-scout:free via OpenRouter API.
- **Frontend**: streamlit-based chat interface with styled chat bubbles and persistent history

---

## Technologies Used

- `transformers` (MarianMT models for translation)
- `sentence-transformers` (distiluse-base-multilingual-cased-v2 for embeddings)
- `bert-score` and `SBERT` (evaluation metrics)
- `streamlit` (frontend interface)
- `litellm` (LLM API interaction via OpenRouter)
- `langdetect` (language detection)

---

## Repository Structure
```
root/
├── Chatbot Friends Evaluation.xlsx
├── crear_indice.py              # Build the vector index (chunks + embeddings).
├── inferencia_interfaz.py       # Backend to handle question answering logic.
├── interfaz.py                  # Streamlit web app interface for the chatbot.
├── helpers/                     # Folder containing all helper modules.
│   ├── conversor.py             # Convert TXT scripts to Markdown.
│   ├── crear_indice.py          # Functions for chunking documents and creating embeddings.
│   ├── hacer_inferencia.py      # Retrieval and LLM inference functions.
│   ├── metrics.py               # Evaluation metrics (BERTScore, SBERT Cosine, Exact Match Rate).
│   ├── LLM_prompts.py           # Custom system prompt for controlled LLM behavior.
│   └── translation.py           # Language detection and translation using MarianMT models.
├── data/                        # Folder with the script datasets.
│   ├── scripts_friends/         # Original Friends TV show scripts in TXT format.
│   └── scripts_friends_md/      # Converted scripts in Markdown format.
├── Indice/                      # Folder where chunks, embeddings, and model are saved.
├── Interfaz-Images/             # Background images for the Streamlit app.
├── .env                         # Environment file storing OpenRouter API key (not pushed to GitHub).
├── Requirements/
│   ├── requirements.txt          # Python dependencies required for the project.
│   └── requirements.txt          # Python dependencies required for the project.

```

---
## OpenRouter API Key Setup

An example `.env` file is already included in the repository. 
You can use the API key we provide or else you can register and obtain a free API key here: https://openrouter.ai/.
This ensures that you have your own usage quota and are not limited by a shared key.

```ini
# Replace this API key with your own OpenRouter key to avoid hitting usage limits.
LLMsAPIkey_v7 = "your_openrouter_api_key_here"

```
---

## How to Run

1. Install requirements:

```
pip install -r Requirements/requirements.txt  
```
2. Make sure the `.env` file is in the root directory

3. Build the `chunks_with_ids.pkl`,`embedding.pkl`, and `model.pkl` files. 
```
python crear_indice.py
``` 
Else paste into the root directory the provided folder `Indice` already extracted.

4. Launch the chatbot interface:
```
streamlit run interfaz.py
```
More commands to run: `python -m streamlit run interfaz.py`, and `py -m streamlit run interfaz.py`

Else you can use the `launch.json` file. Go to Run and Debug (Ctrl+Shift+D) and select `Streamlit: interfaz.py`. 

The first time, it will take some time to run. Sentence-Transformers is downloading its model files (weights, tokenizer, configs) from the Hugging Face hub and shows a tqdm progress bar for each one. It only happens the first time—after the files are cached locally, subsequent runs load them from disk and the download lines disappear. Please be patient and ignore any warnings.

## Evaluation metrics 

See file `Chatbot Friends Evaluation.xlsx` to check the evaluation metrics obtained from our test battery.

* BERTScore: Measures alignment between generated responses and retrieved content.
* SBERT Cosine Similarity: Measures semantic relevance between the question and the generated response.
* Exact Match Rate: Evaluates presence of expected keywords in answers.
