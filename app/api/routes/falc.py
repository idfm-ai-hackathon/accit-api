from fastapi import APIRouter

from app.models.in_text import FalcText, NormalText
from app.models.score_falceur import FalcScore

router = APIRouter()


@router.post("/falcate")
def falcate(in_text: NormalText) -> str:
    """Transforme un texte en version FALC.

    Ce point de terminaison permet de simplifier un texte en une version facile
    à lire et à comprendre.
    Le texte ainsi simplifié peut être compris par les personnes handicapées
    mentales, mais aussi par d'autres comme les personnes dyslexiques,
    malvoyantes, les personnes âgées, les personnes qui maîtrisent mal le
    français.
    """

    return in_text.text


@router.post("/scorecate")
async def score_falc_isation(in_text: FalcText) -> FalcScore:
    """Mesure la qualité de la FALCisation d'un texte.

    Ce point de terminaison permet de noter un texte fourni sur sa facilité à
    être lu et compris. Ce score sera exprimé en pourcentage (entre 0% et 100%).
    Plus le pourcentage est bas, plus le texte fourni est loin de suivre les
    règles FALC (FAcile à Lire et à Comprendre).
    """
    in_text.text

    return FalcScore(good="good", bad="bad", improve="improve", score=0.0)
