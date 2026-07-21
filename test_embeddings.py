from google import genai
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return np.array(result.embeddings[0].values)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

e1 = get_embedding("I love my dog")
e2 = get_embedding("My puppy is great")
e3 = get_embedding("The stock market fell today")

print("dog vs puppy similarity:", cosine_similarity(e1, e2))
print("dog vs stock market similarity:", cosine_similarity(e1, e3))