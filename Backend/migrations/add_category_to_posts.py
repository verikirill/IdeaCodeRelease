from sqlalchemy import create_engine, text
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SQLALCHEMY_DATABASE_URL

def run_migration():
    print("Starting migration: Adding category column to posts table")
    
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Connect and execute SQL
    with engine.connect() as conn:
        try:
            # Check if column already exists
            result = conn.execute(text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.columns "
                "WHERE table_name='posts' AND column_name='category')"
            ))
            column_exists = result.scalar()
            
            if column_exists:
                print("Column category already exists in posts table. Skipping migration.")
                return
                
            # Add column category to posts table with default value
            conn.execute(text(
                "ALTER TABLE posts ADD COLUMN category VARCHAR(50) NOT NULL DEFAULT 'Флудилка'"
            ))
            
            # Commit the transaction
            conn.execute(text("COMMIT"))
            print("Successfully added category column to posts table")
            
        except Exception as e:
            print(f"Migration failed: {str(e)}")
            raise

if __name__ == "__main__":
    run_migration() 