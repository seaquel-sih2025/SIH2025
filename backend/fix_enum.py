#!/usr/bin/env python3
"""
Script to check and fix the user_role enum in the database
"""
import asyncio
from app.db.session import engine
from sqlalchemy import text

async def check_and_fix_enum():
    """Check the current enum values and fix if needed"""
    
    async with engine.begin() as conn:
        try:
            # Check current enum values
            result = await conn.execute(text("""
                SELECT unnest(enum_range(NULL::user_role))::text as enum_value;
            """))
            
            current_values = [row[0] for row in result]
            print("Current enum values:", current_values)
            
            # Expected values
            expected_values = ['citizen', 'official', 'analyst']
            
            # Check if we need to add missing values
            missing_values = [val for val in expected_values if val not in current_values]
            
            if missing_values:
                print(f"Missing enum values: {missing_values}")
                
                # Add missing enum values
                for value in missing_values:
                    print(f"Adding enum value: {value}")
                    await conn.execute(text(f"""
                        ALTER TYPE user_role ADD VALUE IF NOT EXISTS '{value}';
                    """))
                    print(f"✅ Added enum value: {value}")
            else:
                print("✅ All enum values are present")
            
            # Check final enum values
            result = await conn.execute(text("""
                SELECT unnest(enum_range(NULL::user_role))::text as enum_value;
            """))
            
            final_values = [row[0] for row in result]
            print("Final enum values:", final_values)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
            # If the enum doesn't exist, we might need to create it
            if "does not exist" in str(e):
                print("Creating user_role enum...")
                await conn.execute(text("""
                    CREATE TYPE user_role AS ENUM ('citizen', 'official', 'analyst');
                """))
                print("✅ Created user_role enum")

if __name__ == "__main__":
    asyncio.run(check_and_fix_enum())