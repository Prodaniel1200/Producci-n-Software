import os


class Config:
    NOTIFICATIONS_SERVICE_URL = os.getenv("NOTIFICATIONS_SERVICE_URL", "http://notifications_service:5000")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "5"))
