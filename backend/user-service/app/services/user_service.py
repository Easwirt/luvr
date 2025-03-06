from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.schemas import UserCreate, UserUpdate, UserOut
from typing import Optional

class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository
    
    async def create_user(self, db: AsyncSession, user: UserCreate):
        existing_email = await self.user_repository.get_by_email(db, user.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        return await self.user_repository.create(db, user)
    
    async def get_user(self, db: AsyncSession, user_email: str):
        user = await self.user_repository.get_by_email(db, user_email)
        return user
    
    async def update_user(self, db: AsyncSession, user_email: str, user_update: UserUpdate):
            db_user = await self.user_repository.get_by_email(db, user_email)
            if not db_user:
                return None
            
            if user_update.email != user_email:
                existing_email = await self.user_repository.get_by_email(db, user_update.email)
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )

            return await self.user_repository.update(db, db_user.id, user_update)
    
    async def delete_user(self, db: AsyncSession, user_email: str) -> bool:
        return await self.user_repository.delete(db, user_email)
