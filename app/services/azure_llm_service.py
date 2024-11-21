# app/services/llm_service.py
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.core.config import settings
from typing import List


class LLMService:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            model=settings.AZURE_OPENAI_DEPLOYMENT,
            temperature=0.7,
        )

        self.prompt_template = PromptTemplate.from_template("""
Tu es un agent d'assistance de recherche documentaire d'île de France mobilité (IDFM),
à partir des documents donnés donne toujours une réponse provenant du contexte.
Ne donne pas de réponse si le contexte ne te le permet pas.
Répond de manière concise, en trois phrases maximum.
Répond dans la langue de la question.
Inclut toujours un extrait textuel des documents.

Contexte : {context}

Question : {question}

Assistant :""")

    async def generate_response(self, question: str, context: List[str]) -> str:
        """Generate response using LLM."""
        # Combine context into single string
        context_text = "\n".join(context)

        # Format prompt
        prompt = self.prompt_template.format(
            context=context_text,
            question=question
        )

        # Get response from LLM
        response = await self.llm.ainvoke(prompt)
        return response.content
