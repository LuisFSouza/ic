from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def cosi_similarity(texts):
    modelo = SentenceTransformer('all-MiniLM-L6-v2')
    embTexto1 = modelo.encode(texts[0])
    embTexto2 = modelo.encode(texts[1])
    return cosine_similarity([embTexto1], [embTexto2])