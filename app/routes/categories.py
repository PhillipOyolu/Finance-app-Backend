from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app import crud, schemas

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    existing = crud.get_category_by_name_and_type(db, name=category.name, type=category.type)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category '{category.name}' with type '{category.type}' already exists."
        )
    return crud.create_category(db, category)


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    type: Optional[schemas.TransactionTypeEnum] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_categories(db, type=type.value if type else None)


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    category = crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}

