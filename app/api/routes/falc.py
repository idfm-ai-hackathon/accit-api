from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.post(
    "/falcate",
    tags=["falc"],
    openapi_extra={
        "requestBody": {
            "content": {"text/plain"}
        },
        "required": True,
    },
)
def falcate(request: Request) -> str:
    """
    Ce point de terminaison permet de simplifier un texte en une version facile
    à lire et à comprendre.
    Le texte ainsi simplifié peut être compris par les personnes handicapées
    mentales, mais aussi par d'autres comme les personnes dyslexiques,
    malvoyantes, les personnes âgées, les personnes qui maîtrisent mal le
    français.
    """
    raw_text = request.body()

    return raw_text


@router.post(
    "/scorecate",
    tags=["falc"],
    openapi_extra={
        "requestBody": {
            "content": {"text/plain"}
        },
        "required": True,
    },
)
def score_falc_isation(request: Request) -> float:
    """
    Ce point de terminaison permet de noter un texte fourni sur sa facilité à
    être lu et compris. Ce score sera exprimé en pourcentage (entre 0% et 100%).
    Plus le pourcentage est bas, plus le texte fourni est loin de suivre les
    règles FALC (FAcile à Lire et à Comprendre).
    """
    raw_text = request.body()

    return 50.1
