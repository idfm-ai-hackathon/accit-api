from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.core.models import get_model
from app.models.config import get_config


def falcate_a_text(model: BaseChatModel, system_prompt: str, user_prompt: str) -> str:
    custom_rag_prompt = PromptTemplate.from_template(system_prompt)

    rag_chain = (
        {"question": RunnablePassthrough()}
        | custom_rag_prompt
        | model
        | StrOutputParser()
    )

    return rag_chain.invoke(user_prompt)


def falcate(text_to_falcate: str) -> str:
    config = get_config()

    model_to_use = config.falceur.model
    model_config = config.models[model_to_use]

    model = get_model(model_to_use, model_config)

    return falcate_a_text(model, config.falceur.system_prompt, text_to_falcate)


def score_a_text(model: BaseChatModel, system_prompt: str, user_prompt: str) -> dict:
    custom_rag_prompt = PromptTemplate.from_template(system_prompt)

    rag_chain = (
        {"text": RunnablePassthrough()} | custom_rag_prompt | model | JsonOutputParser()
    )

    return rag_chain.invoke(user_prompt)


def falc_text_score(text_to_score: str) -> dict:
    config = get_config()

    model_to_use = config.falc_scorer.model
    model_config = config.models[model_to_use]

    model = get_model(model_to_use, model_config)

    return score_a_text(model, config.falc_scorer.system_prompt, text_to_score)
