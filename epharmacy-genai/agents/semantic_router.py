import numpy as np
from agents.router_examples import INTENT_EXAMPLES
from rag.embeddings import embed_texts


class SemanticRouter:
    def __init__(self, examples_dict=None):
        # allow reuse with different label sets
        self.examples = examples_dict or INTENT_EXAMPLES
        self.intent_vectors = self._build_index()

    # -----------------------------
    # BUILD INTENT CENTROIDS
    # -----------------------------
    def _build_index(self):
        index = {}
        for intent, examples in self.examples.items():
            vecs = embed_texts(examples)     # ✅ pass list at once
            index[intent] = np.mean(vecs, axis=0)
        return index

    # -----------------------------
    # ROUTE QUERY
    # -----------------------------
    def route(self, query: str):
        q_vec = embed_texts([query])[0]     # ✅ wrap in list, take vector

        scores = {}
        for intent, vec in self.intent_vectors.items():
            scores[intent] = self.cosine_similarity(q_vec, vec)

        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        return best_intent, best_score, scores

    # -----------------------------
    # SIMILARITY
    # -----------------------------
    @staticmethod
    def cosine_similarity(a, b):
        return float(
            np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        )
