
from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

vector = model.encode("UPI payment failed")

print("Vector dimension:", len(vector))