import motor.motor_asyncio  # For MongoDB (or use another library for other DBs)

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["daily_goals"]

async def init_db():
    # Example: Create indices or seed data if necessary
    print("Database initialized.")
