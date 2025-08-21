from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_query(text: str):
    model = get_model()
    emb = model.encode(text, convert_to_numpy=True)
    normalized_emb = emb / np.linalg.norm(emb)
    return normalized_emb.tolist()


# q = "A frequency modulated (coherent) laser detection and ranging system"
# sample = embed_query(q)
# print(sample)