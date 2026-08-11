from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from database import get_db
from models import Admin, ITAsset
from schemas import ITAssetCreate, ITAssetResponse, ITAssetUpdate

router = APIRouter()


@router.get("", response_model=List[ITAssetResponse])
def get_it_assets(
    category: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """List IT hardware assets with optional category and status filters."""
    query = db.query(ITAsset)
    if category and category != "All":
        query = query.filter(ITAsset.category == category)
    if status_filter and status_filter != "All":
        query = query.filter(ITAsset.status == status_filter)

    return query.order_by(ITAsset.created_at.desc()).all()


@router.post("", response_model=ITAssetResponse, status_code=status.HTTP_201_CREATED)
def create_it_asset(
    payload: ITAssetCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Register new IT asset item."""
    existing = db.query(ITAsset).filter(ITAsset.asset_tag == payload.asset_tag).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An asset with this asset tag already exists.",
        )

    asset = ITAsset(
        asset_name=payload.asset_name,
        asset_tag=payload.asset_tag,
        category=payload.category,
        serial_number=payload.serial_number,
        admin_id=payload.admin_id,
        status=payload.status,
        assigned_date=payload.assigned_date,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.patch("/{asset_id}", response_model=ITAssetResponse)
def update_it_asset(
    asset_id: int,
    payload: ITAssetUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Update IT asset assignment or status."""
    asset = db.query(ITAsset).filter(ITAsset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IT asset item not found.",
        )

    if payload.asset_name is not None:
        asset.asset_name = payload.asset_name
    if payload.category is not None:
        asset.category = payload.category
    if payload.serial_number is not None:
        asset.serial_number = payload.serial_number
    if payload.admin_id is not None:
        asset.admin_id = payload.admin_id
    if payload.status is not None:
        asset.status = payload.status
    if payload.assigned_date is not None:
        asset.assigned_date = payload.assigned_date

    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_it_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete an IT asset item."""
    asset = db.query(ITAsset).filter(ITAsset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IT asset item not found.",
        )

    db.delete(asset)
    db.commit()
    return None
