import os

class Config:
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = int(os.getenv("FLASK_RUN_PORT", 3000))