from typing import Iterable, List, Tuple
from ..models import Transaction
from .llm import get_openai

SYSTEM_PROMPT = (
    "Tu es un assistant financier qui assigne une catégorie métier à chaque transaction. "
    "Retourne UNIQUEMENT la catégorie pour chaque ligne, une par ligne, sans autre texte."
)

CATEGORIES = [
    "Logement", "Transport", "Alimentation", "Santé", "Divertissement",
    "Abonnements", "Voyage", "Services", "Salaire", "Ventes", "Autres",
]


def build_prompt(txs: Iterable[Transaction]) -> str:
    lines = [
        "Colonnes: id | date | montant | direction | description",
    ]
    for t in txs:
        lines.append(f"{t.id}|{t.date}|{t.amount}|{t.direction}|{t.description}")
    lines.append("\nCatégories possibles: " + ", ".join(CATEGORIES))
    lines.append("\nPour chaque transaction, renvoie UNIQUEMENT une catégorie parmi la liste ci-dessus.")
    return "\n".join(lines)


def categorize_transactions(txs: List[Transaction]) -> List[Tuple[Transaction, str]]:
    if not txs:
        return []
    client = get_openai()
    user_prompt = build_prompt(txs)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )
    content = resp.choices[0].message.content.strip()
    cats = [line.strip() for line in content.splitlines() if line.strip()]
    # align sizes; fallback to "Autres"
    while len(cats) < len(txs):
        cats.append("Autres")
    return list(zip(txs, cats[: len(txs)]))
