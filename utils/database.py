from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB Atlas"""
    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL not found in environment variables")
    
    db.client = AsyncIOMotorClient(mongodb_url, server_api=ServerApi('1'))
    db.db = db.client.socialtab
    
    # Test connection
    try:
        await db.client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("🔌 MongoDB connection closed")

def get_database():
    """Get database instance"""
    return db.db
