from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session
from ..db import get_session
import csv, io, json
from ..services.recon import parse_bank_rows, match_rows
from ..services.security import require_roles

router = APIRouter(prefix="/reconciliation", tags=["reconciliation"])


@router.post("/upload")
def upload_statement(file: UploadFile = File(...), session: Session = Depends(get_session), user=Depends(require_roles(["admin","finance_manager","accountant"]))):
    content = file.file.read()
    rows = []
    if file.filename.endswith(".csv"):
        reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
        rows = [r for r in reader]
    elif file.filename.endswith(".json"):
        rows = json.loads(content.decode("utf-8"))
    else:
        return {"error": "format non supporté (csv,json)"}
    parsed = parse_bank_rows(rows)
    matches = match_rows(session, parsed)
    return {"matched": sum(1 for m in matches if m.status=="matched"), "total": len(matches)}
