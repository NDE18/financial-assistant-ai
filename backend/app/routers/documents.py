from fastapi import APIRouter, UploadFile, File, Depends
from ..db import get_session
from sqlmodel import Session
from ..models import Document
import os
from datetime import datetime
from ..services.security import require_roles

router = APIRouter(prefix="/documents", tags=["documents"])

STORAGE_DIR = os.path.join("storage", "docs")
os.makedirs(STORAGE_DIR, exist_ok=True)


@router.post("/upload")
def upload_document(file: UploadFile = File(...), session: Session = Depends(get_session), user=Depends(require_roles(["admin","finance_manager","accountant"]))):
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    stored_name = f"{ts}_{file.filename}"
    stored_path = os.path.join(STORAGE_DIR, stored_name)
    with open(stored_path, "wb") as f:
        f.write(file.file.read())
    doc = Document(original_filename=file.filename, stored_path=stored_path)
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc
