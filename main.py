# pip install sentence-transformers numpy rapidfuzz
from sentence_transformers import SentenceTransformer
import numpy as np
import unicodedata, re
from rapidfuzz import fuzz

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

catalogo = [
    {"sku": "SKU-001", "descricao": "Tênis Run Pro Masculino Tam 42"},
    {"sku": "SKU-003", "descricao": "Tênis Run Pro Masculino Tam 41"},
    {"sku": "SKU-002", "descricao": "Camiseta Dry Fit Azul G"},
]

def normalizar(texto):
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", texto)  # ANTES do lower
    t = t.lower()
    t = unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"\s+", " ", t).strip()
    return t

# catálogo: normaliza UMA vez e gera os vetores
desc_norm = [normalizar(c["descricao"]) for c in catalogo]
emb_catalogo = model.encode(desc_norm, normalize_embeddings=True)

# nome da loja
nome_loja = "Tenis RunPro 42"
nome_norm = normalizar(nome_loja)
emb_nome = model.encode([nome_norm], normalize_embeddings=True)[0]

# score combinado POR CANDIDATO, no catálogo inteiro
scores_emb = emb_catalogo @ emb_nome
scores_fuzzy = np.array([
    fuzz.token_set_ratio(nome_norm, d) / 100 for d in desc_norm
])

print(f"Scores emb: {scores_emb}")
print(f"Scores fuzzy: {scores_fuzzy}")

scores_finais = 0.5 * scores_emb + 0.5 * scores_fuzzy

print(f"Scores finais: {scores_finais}")

melhor_idx = int(np.argmax(scores_finais))
score = float(scores_finais[melhor_idx])

ordenados = np.sort(scores_finais)[::-1]
gap = ordenados[0] - ordenados[1]

print(gap)

print(f"Melhor: {catalogo[melhor_idx]['sku']} | emb={scores_emb[melhor_idx]:.2f} fuzzy={scores_fuzzy[melhor_idx]:.2f}")

if score >= 0.85 and gap >= 0.03:
    print(f"Match automático: {catalogo[melhor_idx]['sku']} ({score:.2f})")
elif score >= 0.70:
    print("Ambíguo → LLM desempate ou revisão humana")
else:
    print("Sem match confiável — revisar manualmente")