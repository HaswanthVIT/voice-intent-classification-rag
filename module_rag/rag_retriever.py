# module_rag/rag_retriever.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3


class RAGRetriever:

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        self.client = chromadb.Client(
            Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledge_v1"
        )

        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        if self.collection.count() > 0:
            return  # Prevent duplicate inserts

        documents = [
            # Past calls
            "CALL_1021: Tamil speaker, confident tone, site visit requested, converted successfully",
            "CALL_1044: Budget discussed but hesitant tone, did not convert",
            "CALL_1102: Multiple questions about loan and possession, converted",

            # Business rules
            "RULE_01: Budget and site visit request indicates strong intent",
            "RULE_02: High engagement and confident tone increases intent score",
            "RULE_03: Negative sentiment reduces likelihood of purchase",

            # Domain knowledge
            "DOMAIN_01: Real estate buyers often ask about possession date before purchase",
            "DOMAIN_02: Loan discussions indicate serious financial consideration"
        ]

        ids = [
            "CALL_1021",
            "CALL_1044",
            "CALL_1102",
            "RULE_01",
            "RULE_02",
            "RULE_03",
            "DOMAIN_01",
            "DOMAIN_02"
        ]

        embeddings = self.model.encode(documents).tolist()

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )

    def retrieve(self, query_text: str):
        try:
            query_embedding = self.model.encode([query_text]).tolist()

            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=TOP_K
            )

            retrieved = []
            for i in range(len(results["ids"][0])):
                retrieved.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i]
                })

            return retrieved

        except Exception:
            return []