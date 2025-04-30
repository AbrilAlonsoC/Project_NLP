from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
import json
from litellm import completion

old_init = requests.Session.__init__
 
def new_init(self):
    old_init(self)
    self.verify = False
 
requests.Session.__init__ = new_init



# Function to get the most similar chunks
def get_similar_chunks(question, chunks, embeddings, model, top_n):
    question_embedding = model.encode([question])
    similarities = cosine_similarity(question_embedding, embeddings)[0]
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    return [(chunks[i], similarities[i]) for i in top_indices]


# Function to get the response from a LLM
def get_LLM_response(proveedor,apikey,endpoint_model,user_prompt,system_prompt):

  try:
    response = completion(
      model=proveedor.lower()+"/"+endpoint_model,
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
      ],
      api_key=apikey,
      temperature=0.2,
      presence_penalty=0.3,
      top_p=0.7,
      frequency_penalty=1,
      ssl_verify=False  
      )
    return response.choices[0].message.content
  
  except requests.exceptions.RequestException as e:
    # Deal with network or server errors
    print(f"Error de red o del servidor: {e}")
    return "ERROR"

  except (KeyError, IndexError) as e:
    # Manage unexpected response structure errors
    print(f"Error en la estructura de la respuesta: {e}")
    return "ERROR"

  except json.JSONDecodeError as e:
    # Manage JSON decoding errors
    print(f"Error al decodificar la respuesta JSON: {e}")
    return "ERROR"

  except Exception as e:
    # Capture any other unexpected error
    print(f"Error inesperado: {e}")
    return "ERROR"