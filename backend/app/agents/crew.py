from crewai import Agent, Task, Crew
from ..core.config import settings
from ..services.llm import get_openai

# Minimal CrewAI setup for POC: categorization + reporting orchestration

def make_agents():
    tx_agent = Agent(
        role="Gestionnaire de transactions",
        goal="Catégoriser et enrichir les écritures comptables",
        backstory=(
            "Expert en comptabilité analytique, il connaît les normes et les meilleures pratiques"
        ),
        verbose=False,
        allow_delegation=False,
        llm="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
    )

    report_agent = Agent(
        role="Contrôleur de gestion",
        goal="Rédiger des synthèses financières claires et actionnables",
        backstory="10 ans d'expérience en reporting et pilotage de la performance",
        verbose=False,
        allow_delegation=False,
        llm="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
    )

    orchestrator = Agent(
        role="Orchestrateur",
        goal="Coordonner les agents métiers pour livrer un résultat utile",
        backstory="Chef de mission qui sait qui fait quoi et dans quel ordre",
        verbose=False,
        allow_delegation=True,
        llm="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
    )

    return orchestrator, tx_agent, report_agent


def categorize_with_crew(rows: list[dict]) -> list[str]:
    orchestrator, tx_agent, _ = make_agents()

    description = (
        "Attribue une catégorie à chaque transaction. Réponds avec une catégorie par ligne, "
        "dans le même ordre que l'entrée. Catégories métiers usuelles (FR)."
    )
    content = "\n".join(
        f"{r['id']} | {r['date']} | {r['amount']} | {r['direction']} | {r.get('description','')}"
        for r in rows
    )

    t = Task(description=description + "\n\n" + content, agent=tx_agent, expected_output="liste de catégories")
    crew = Crew(agents=[orchestrator, tx_agent], tasks=[t])
    result = crew.kickoff()
    lines = [ln.strip() for ln in str(result).splitlines() if ln.strip()]
    while len(lines) < len(rows):
        lines.append("Autres")
    return lines[: len(rows)]


def summarize_with_crew(payload: dict) -> str:
    orchestrator, _, report_agent = make_agents()
    t = Task(
        description=(
            "Rédige un résumé (<100 mots) des indicateurs du mois et propose 2 actions. "
            f"Données: {payload}"
        ),
        agent=report_agent,
        expected_output="texte concis en français",
    )
    crew = Crew(agents=[orchestrator, report_agent], tasks=[t])
    result = crew.kickoff()
    return str(result).strip()
