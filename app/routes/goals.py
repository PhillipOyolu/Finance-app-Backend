from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.core_auth import get_current_user
from app import crud, schemas

router = APIRouter(prefix="/goals", tags=["Savings Goals"])


@router.post("/", response_model=schemas.SavingsGoal)
def create_goal(data: schemas.SavingsGoalCreate,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    return crud.create_savings_goal(db, data, user.id)


@router.get("/", response_model=list[schemas.SavingsGoal])
def list_goals(db: Session = Depends(get_db),
               user=Depends(get_current_user)):
    return crud.get_savings_goals(db, user.id)


@router.put("/{goal_id}", response_model=schemas.SavingsGoal)
def update_goal(goal_id: int,
                data: schemas.SavingsGoalUpdate,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    return crud.update_savings_goal(db, goal_id, data)


@router.delete("/{goal_id}")
def delete_goal(goal_id: int,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    return crud.delete_savings_goal(db, goal_id)


@router.post("/{goal_id}/contribute", response_model=schemas.SavingsGoal)
def contribute(goal_id: int,
               amount: float,
               db: Session = Depends(get_db),
               user=Depends(get_current_user)):
    return crud.contribute_to_goal(db, goal_id, amount)
