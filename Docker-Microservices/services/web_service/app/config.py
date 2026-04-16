import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:5000")
    AGENDA_SERVICE_URL = os.getenv("AGENDA_SERVICE_URL", "http://agenda-service:5000")
    CONTACT_SERVICE_URL = os.getenv(
        "CONTACT_SERVICE_URL", "http://contact-service:5000"
    )
    INTEGRATIONS_SERVICE_URL = os.getenv(
        "INTEGRATIONS_SERVICE_URL", "http://integrations-service:5000"
    )
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
