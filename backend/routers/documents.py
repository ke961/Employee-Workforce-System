from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_admin, require_hr_or_admin
from database import get_db
from models import Admin, CompanyDocument, DocumentAcknowledgment
from schemas import CompanyDocumentCreate, CompanyDocumentResponse

router = APIRouter()


@router.get("", response_model=List[CompanyDocumentResponse])
def get_company_documents(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List company policy documents with current user acknowledgment status."""
    docs = db.query(CompanyDocument).order_by(CompanyDocument.created_at.desc()).all()
    user_ack_ids = {
        ack.document_id
        for ack in db.query(DocumentAcknowledgment)
        .filter(DocumentAcknowledgment.admin_id == current_admin.id)
        .all()
    }

    results = []
    for doc in docs:
        d = CompanyDocumentResponse.model_validate(doc)
        d.is_acknowledged = doc.id in user_ack_ids
        results.append(d)

    return results


@router.post("", response_model=CompanyDocumentResponse, status_code=status.HTTP_201_CREATED)
def create_company_document(
    payload: CompanyDocumentCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(require_hr_or_admin),
):
    """Add a new company policy document (Requires HR or Admin role)."""
    doc = CompanyDocument(
        title=payload.title,
        category=payload.category,
        summary=payload.summary,
        file_url=payload.file_url,
        version=payload.version,
        requires_acknowledgment=payload.requires_acknowledgment,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    d = CompanyDocumentResponse.model_validate(doc)
    d.is_acknowledged = False
    return d


@router.post("/{document_id}/acknowledge")
def acknowledge_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Mark a document as read & acknowledged by the current employee."""
    doc = db.query(CompanyDocument).filter(CompanyDocument.id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    existing = (
        db.query(DocumentAcknowledgment)
        .filter(
            DocumentAcknowledgment.document_id == document_id,
            DocumentAcknowledgment.admin_id == current_admin.id,
        )
        .first()
    )

    if not existing:
        ack = DocumentAcknowledgment(
            document_id=document_id,
            admin_id=current_admin.id,
        )
        db.add(ack)
        db.commit()

    return {"message": "Document successfully acknowledged.", "document_id": document_id}
