import os
from dotenv import load_dotenv
from pathlib import Path

class DBConfig:

    def __init__(self):
        CURRENT_DIR = Path(__file__).resolve().parent
        ENV_FILE = CURRENT_DIR / '.env'
        load_dotenv(dotenv_path=ENV_FILE)  # Load environment variables from .env file

        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')

    def get_connection_string(self):
        return (f"mysql+mysqlconnector://"  # <-- THIS IS THE CRITICAL PART
                f"{self.user}:{self.password}@"
                f"{self.host}/{self.db_name}")
    
