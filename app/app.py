# /app.py

from initializers.service_initializer import initialize_services
from initializers.manager_initializer import initialize_managers
from config.config_loader import load_punishment_doctrine

print("🚀 PersonalPM is booting...")

# 1. Load Punishment Doctrine
punishment_doctrine = load_punishment_doctrine()

# 2. Initialize all services
services = initialize_services(punishment_doctrine)

# 3. Initialize all managers
managers = initialize_managers(services)

# Now you can easily hook in:
# - FastAPI server
# - Discord/Telegram messaging
# - Cronjobs or scheduled ritual triggers

print("✅ PersonalPM fully initialized and ready to dominate.")
