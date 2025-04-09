import os
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

def load_friends_scripts(data_folder):
    """
    Loads all Friends scripts from the specified folder into LangChain Documents.
    """
    documents = []
    for filename in sorted(os.listdir(data_folder)):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
                metadata = {
                    "filename": filename,
                    "season": filename[1:3],
                    "episode": filename[5:7],
                }
                documents.append(Document(page_content=text, metadata=metadata))
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Splits a list of LangChain Documents into smaller chunks.
    """
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_documents(documents)
