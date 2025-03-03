from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.core.schemas import UserCreate, UserUpdate, UserOut
from app.services.user_service import UserService
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session 

router = APIRouter()

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    user: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends()
):
    return await user_service.create_user(db, user)

@router.get("/users/{user_email}", response_model=UserOut)
async def get_user_profile(
    user_email: str,
    db: Session = Depends(get_db),
    user_service: UserService = Depends()
):
    user = await user_service.get_user(db, user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with ID {user_email} not found"
        )
    return user

@router.put("/users/{user_email}", response_model=UserOut)
async def update_user_profile(
    user_email: str,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends()
):
    updated_user = await user_service.update_user(db, user_email, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with email {user_email} not found"
        )
    return updated_user

@router.delete("/users/{user_email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
    user_email: str,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends()
):
    success = user_service.delete_user(db, user_email)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with ID {user_email} not found"
        )
    return None