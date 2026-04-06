import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:5000")
    AGENDA_SERVICE_URL = os.getenv("AGENDA_SERVICE_URL", "http://agenda_service:5000")
    CONTACT_SERVICE_URL = os.getenv("CONTACT_SERVICE_URL", "http://contact_service:5000")
    INTEGRATIONS_SERVICE_URL = os.getenv("INTEGRATIONS_SERVICE_URL", "http://integrations_service:5000")
    REQUEST_TIMEOUT = 10
