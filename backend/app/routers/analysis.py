from fastapi import APIRouter

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/insights")
def insights():
    # Placeholder for advanced analysis (trends, KPI)
    return {
        "top_categories": [{"category": "Food", "amount": 320.0}],
        "anomalies": [],
        "recommendations": [
            "Réduire les dépenses de restauration de 10% pour rester sous le budget.",
        ],
    }
