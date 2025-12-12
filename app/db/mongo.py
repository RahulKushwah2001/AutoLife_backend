# from motor.motor_asyncio import AsyncIOMotorClient
# from app.core.config import settings

# client = AsyncIOMotorClient(settings.MONGO_URL)
# db = client[settings.DB_NAME]


from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

if not settings.MONGO_URL:
    print("⚠️ MongoDB disabled — no MONGO_URL found.")
    client = None
    db = None
else:
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.DB_NAME]
