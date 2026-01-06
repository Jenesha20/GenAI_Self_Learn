from typing import Dict, List
import numpy as np
from agents.router_examples import INTENT_EXAMPLES
from rag.embeddings import embed_texts


class SemanticRouter:
    def __init__(self):
        self.intent_vectors = self._build_index()

    def _build_index(self):
        index = {}
        for intent, examples in INTENT_EXAMPLES.items():
            vecs = [embed_texts(e) for e in examples]
            index[intent] = np.mean(vecs, axis=0)  # centroid
        return index

    def route(self, query: str):
        q_vec = embed_texts(query)

        scores = {}
        for intent, vec in self.intent_vectors.items():
            scores[intent] = self.cosine_similarity(q_vec, vec)

        # best intent + score
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        return best_intent, best_score, scores

    @staticmethod
    def cosine_similarity(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
