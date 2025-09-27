#!/usr/bin/env python3
"""
Script to create a test user for authentication testing
"""
import asyncio
import uuid
from app.db.session import get_db
from app.db.models import User, UserRole
from app.core.security import hash_password

async def create_test_user():
    """Create a test user in the database"""
    
    # Get database session
    async for db in get_db():
        try:
            # Check if user already exists
            from sqlalchemy.future import select
            query = select(User).where(User.email == "test@example.com")
            result = await db.execute(query)
            existing_user = result.scalars().first()
            
            if existing_user:
                print("Test user already exists!")
                print(f"Email: {existing_user.email}")
                print(f"Role: {existing_user.role}")
                return
            
            # Create new test user
            test_user = User(
                id=uuid.uuid4(),
                email="test@example.com",
                full_name="Test User",
                phone="1234567890",
                hashed_password=hash_password("password123"),
                role=UserRole.citizen,
                is_active=True,
                reputation_score=100,
                is_verified=False
            )
            
            db.add(test_user)
            await db.commit()
            await db.refresh(test_user)
            
            print("✅ Test user created successfully!")
            print(f"Email: {test_user.email}")
            print(f"Password: password123")
            print(f"Role: {test_user.role}")
            print(f"ID: {test_user.id}")
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            await db.rollback()
        finally:
            break

if __name__ == "__main__":
    asyncio.run(create_test_user())