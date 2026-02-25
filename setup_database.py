import os
from utils.database import PostgreSQLManager
from dotenv import load_dotenv

def setup_database():
    """Initialize the database with sample data"""
    load_dotenv()
    
    print("🚀 Setting up Coconut LeafGuard Database...")
    
    # This will automatically create tables
    db = PostgreSQLManager()
    
    # Add sample data (optional)
    print("✅ Database setup completed!")
    
    # Test connection
    try:
        result = db.fetch_one("SELECT version()")
        print(f"📊 PostgreSQL Version: {result['version']}")
        print("🎉 Database is ready to use!")
    except Exception as e:
        print(f"❌ Database test failed: {e}")

if __name__ == "__main__":
    setup_database()