from typing import List
from .vector_store import SimpleVectorStore

class FAQRAG:
    def __init__(self, store: SimpleVectorStore):
        self.store = store

    async def answer(self, question: str) -> str:
        results = await self.store.query(question, top_k=3)
        if not results:
            return (
                "I’m not fully sure about that. "
                "Please call the clinic directly for the most accurate information."
            )

        snippets = []
        for doc, score in results:
            snippets.append(f"- {doc.get('title', 'Info')}: {doc['content']}")
        joined = "\n".join(snippets)

        return (
            "Here’s what I found based on our clinic information:\n\n"
            f"{joined}\n\n"
            "If anything is still unclear, I can try to clarify further."
        )
