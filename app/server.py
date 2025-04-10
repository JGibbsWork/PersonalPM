# /server.py

from fastapi import FastAPI
from config.config_loader import load_punishment_doctrine
from initializers.service_initializer import initialize_services
from initializers.manager_initializer import initialize_managers
from shared import global_objects
from api import ritual

app = FastAPI(
    title="PersonalPM Core",
    description="FastAPI server for Rituals, Punishment, Obedience",
    version="0.1.0"
)

# Load doctrine
punishment_doctrine = load_punishment_doctrine()

# Initialize services + managers
services = initialize_services(punishment_doctrine)
managers = initialize_managers(services)

# 🧠 SET GLOBAL OBJECTS (this part is critical!)
global_objects.services = services
global_objects.managers = managers

# Mount routers
app.include_router(ritual.router, prefix="/ritual")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
