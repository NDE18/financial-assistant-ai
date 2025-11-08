from .llm import get_openai


def summarize_month(income: float, expense: float, net: float, year: int, month: int) -> str:
    client = get_openai()
    prompt = (
        f"Mois {month}/{year}. Recettes: {income:.2f}. Dépenses: {expense:.2f}. Net: {net:.2f}. "
        "Rédige une courte synthèse (<100 mots) et propose 2 actions concrètes."
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un contrôleur de gestion concis."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
