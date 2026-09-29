from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app import crud, schemas, models

router = APIRouter(prefix="/goals", tags=["Savings Goals"])

@router.post("/", response_model=schemas.SavingsGoal, status_code=status.HTTP_201_CREATED)
def create_goal(
    data: schemas.SavingsGoalCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud.create_savings_goal(db, data, user.id)


@router.get("/", response_model=List[schemas.SavingsGoal])
def list_goals(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud.get_savings_goals(db, user.id)


@router.put("/{goal_id}", response_model=schemas.SavingsGoal)
def update_goal(
    goal_id: int,
    data: schemas.SavingsGoalUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    updated = crud.update_savings_goal(db, goal_id, data, user.id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return updated


@router.delete("/{goal_id}", status_code=status.HTTP_200_OK)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    deleted = crud.delete_savings_goal(db, goal_id, user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return {"message": "Goal successfully deleted"}


@router.post("/{goal_id}/contribute", response_model=schemas.SavingsGoal)
def contribute(
    goal_id: int,
    amount: float = Query(..., gt=0, description="Contribution amount must be greater than zero"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    goal = db.query(models.SavingsGoal).filter(
        models.SavingsGoal.id == goal_id,
        models.SavingsGoal.user_id == user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    goal.current_amount += amount
    db.commit()
    db.refresh(goal)
    return goal
