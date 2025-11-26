# config.py
import streamlit as st
import ssl
from urllib.request import urlopen
from urllib.parse import quote_plus

class DBConfig:
    def __init__(self):
        # Lấy thông tin từ st.secrets (Streamlit Cloud) hoặc fallback .env
        try:
            tidb = st.secrets["tidb"]
        except:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            tidb = {
                "host": os.getenv("DB_HOST"),
                "port": int(os.getenv("DB_PORT", 4000)),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME"),
            }

        self.host = tidb["host"]
        self.port = tidb.get("port", 4000)
        self.user = tidb["user"]
        self.password = tidb["password"]
        self.database = tidb["database"]

    def get_connection_string(self):
        # Tự động tải CA certificate của TiDB Cloud
        ca_url = "https://docs.tidb.cloud/certificates/root.crt"
        ca_content = urlopen(ca_url).read().decode("utf-8")

        return (
            f"mysql+mysqlconnector://"
            f"{self.user}:{quote_plus(self.password)}@"
            f"{self.host}:{self.port}/{self.database}"
            f"?ssl_ca={quote_plus(ca_content)}"
            f"&ssl_verify_cert=true"
            f"&ssl_disabled=false"
        )