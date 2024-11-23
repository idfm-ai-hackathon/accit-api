from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.core.models import get_model
from app.models.config import get_config


def falcate_a_text_with_model_and_instructions(
    model: BaseChatModel,
    system_prompt: str,
    text: str,
) -> str:
    custom_rag_prompt = PromptTemplate.from_template(system_prompt)

    rag_chain = (
        {"question": RunnablePassthrough()}
        | custom_rag_prompt
        | model
        | StrOutputParser()
    )

    return rag_chain.invoke(text)


def falcate_text(text_to_falcate: str) -> str:
    """Transforme un texte en version FALC.

    Le modèle et le système prompt sont récupérés depuis la configuration.
    """
    config = get_config()

    model_to_use = config.falceur.model
    model_config = config.models[model_to_use]

    model = get_model(model_to_use, model_config)

    return falcate_a_text_with_model_and_instructions(
        model, config.falceur.system_prompt, text_to_falcate
    )
