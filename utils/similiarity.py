# utils/similiarity.py

from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def flatten_resume_json(resume_data: Dict[str, Any]) -> str:
    parts = []

    personal = resume_data.get("personal_info", {})
    parts.append(" ".join(str(v) for v in personal.values() if v))

    for exp in resume_data.get("work_experience", []):
        parts.append(" ".join([exp.get("company", ""), exp.get("title", ""), exp.get("duration", "")]))
        parts.extend(exp.get("responsibilities", []))

    for edu in resume_data.get("education", []):
        parts.append(" ".join([edu.get("degree", ""), edu.get("institution", ""), edu.get("graduation_year", "")]))

    for key in ["skills", "tech_stack", "achievements", "certifications"]:
        items = resume_data.get(key, [])
        if items:
            parts.extend(items)

    return "\n".join(parts)


def create_faiss_index(documents: List[str]) -> tuple[faiss.IndexFlatL2, np.ndarray]:
    """
    Create a FAISS index for efficient similarity search
    
    Args:
        documents: List of document texts to index
        
    Returns:
        tuple: (faiss_index, document_embeddings)
    """
    embeddings = model.encode(documents, convert_to_numpy=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, embeddings


def compare_with_resume(parsed_resume: Dict[str, Any], docs: List[str]) -> List[Dict[str, Any]]:
    query_text = flatten_resume_json(parsed_resume)
    query_embedding = model.encode([query_text], convert_to_numpy=True)

    index, doc_embeddings = create_faiss_index(docs)
    distances, indices = index.search(query_embedding, k=3)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "document": docs[idx],
            "similarity_score": float(1 / (1 + distances[0][i]))  # Inverse L2 distance as pseudo similarity
        })
    return results
