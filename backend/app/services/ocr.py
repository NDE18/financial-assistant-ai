import pdfplumber
from fastapi import UploadFile
from .llm import get_openai


def extract_text_from_pdf(file: UploadFile) -> str:
    with pdfplumber.open(file.file) as pdf:
        texts = []
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return "\n".join(texts)


def parse_invoice_text(text: str) -> dict:
    client = get_openai()
    prompt = (
        "Extrait les champs d'une facture (counterparty, amount, currency, due_date YYYY-MM-DD). "
        "Réponds en JSON compact.\n\n" + text[:4000]
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu structures des données de facture."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    import json
    import re
    content = resp.choices[0].message.content.strip()
    # Extract JSON from response
    m = re.search(r"\{.*\}", content, re.S)
    data = json.loads(m.group(0)) if m else {}
    return data
