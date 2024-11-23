from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.core.models import get_model
from app.db.models.user_feedback import FalcUserFeedBack
from app.models.config import get_config


def score_a_text_with_model_and_instruction(
    model: BaseChatModel, system_prompt: str, user_prompt: str
) -> dict:
    custom_rag_prompt = PromptTemplate.from_template(system_prompt)

    rag_chain = (
        {"text": RunnablePassthrough()} | custom_rag_prompt | model | JsonOutputParser()
    )

    return rag_chain.invoke(user_prompt)


def score_text_on_falc(text_to_score: str) -> dict:
    """Mesure la qualité de la FALCisation d'un texte.

    Le modèle et le système prompt sont récupérés depuis la configuration.
    """
    config = get_config()

    model_to_use = config.falc_scorer.model
    model_config = config.models[model_to_use]

    model = get_model(model_to_use, model_config)

    user_feedbacks = parse_falc_user_feedback(FalcUserFeedBack.get_all())

    system_prompt = config.falc_scorer.system_prompt

    if config.falc_scorer.enrich_with_user_feedback:
        system_prompt = (
            f"{system_prompt}\n\nVoici des examples de textes "
            f"précédemment générés :\n{user_feedbacks}"
        )

    return score_a_text_with_model_and_instruction(model, system_prompt, text_to_score)


def parse_falc_user_feedback(feedbacks: list[FalcUserFeedBack]) -> str:
    for feedback in feedbacks:
        if feedback.understood:
            return (
                f"Le texte simplifié suivant a été compris : '{feedback.falc_text}'. "
                f"Le texte original était : '{feedback.non_falc_text}'"
            )
        else:
            return (
                f"Le texte simplifié suivant n'a PAS été compris : '{feedback.falc_text}'. "
                f"Il faudrait que {feedback.non_falc_text} suivent mieux les règles énoncées."
            )
