import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv  # Optional, for local dev fallback

class DBConfig:
    def __init__(self):
        # Load .env for local development (optional)
        CURRENT_DIR = Path(__file__).resolve().parent
        ENV_FILE = CURRENT_DIR / '.env'
        load_dotenv(dotenv_path=ENV_FILE)

        # Prioritize st.secrets (for Streamlit Cloud); fallback to env vars
        try:
            tidb_secrets = st.secrets["tidb"]
            self.host = tidb_secrets["host"]
            self.port = tidb_secrets.get("port", 3306)  # Default MySQL port if not specified
            self.user = tidb_secrets["user"]
            self.password = tidb_secrets["password"]
            self.db_name = tidb_secrets["database"]
        except KeyError:
            # Fallback to env vars (for local or non-Streamlit envs)
            self.host = os.getenv('DB_HOST')
            self.port = int(os.getenv('DB_PORT', 3306))
            self.user = os.getenv('DB_USER')
            self.password = os.getenv('DB_PASSWORD')
            self.db_name = os.getenv('DB_NAME')

    def get_connection_string(self):
        return (
            f"mysql+mysqlconnector://"
            f"{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.db_name}"
        )