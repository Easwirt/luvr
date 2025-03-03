from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.models import User
from app.core.schemas import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    async def create(self, db: AsyncSession, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    async def get_by_id(self, db: AsyncSession, user_id: str) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    async def get_by_email(self, db: AsyncSession, email: str) -> User:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_by_username(self, db: AsyncSession, username: str) -> User:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()
    
    async def update(self, db: AsyncSession, user_id: str, user_update: UserUpdate) -> User:
        db_user = await self.get_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
            
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    async def delete(self, db: AsyncSession, user_email: str) -> bool:
        db_user = await self.get_by_email(db, user_email)
        if not db_user:
            return False
        
        await db.delete(db_user)
        await db.commit()
        return True