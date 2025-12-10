from app.db.mongo import db

collection = db["users"]

async def find_user_by_email(email: str):
    return await collection.find_one({"email": email})

async def create_user(user_data: dict):
    result = await collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    return user_data
