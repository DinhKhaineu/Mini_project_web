import pandas as pd
from sqlalchemy import create_engine, text
from config import DBConfig

class MySQLClient:
    def __init__(self, config: DBConfig):
        connection_string = config.get_connection_string()
        self.engine = create_engine(connection_string)
        print("Database connection established.")

    def query_to_data_frame(self, sql: str) -> pd.DataFrame:
        try: 
            with self.engine.connect() as connection:
                df = pd.read_sql_query(text(sql), connection)
                return df
        except Exception as e:
            print(f"Error occurred while querying the database: {e}")
            return pd.DataFrame()
        
    def execute_query(self, sql: str, params: dict = None) -> bool:
        try: 
            with self.engine.connect() as connection:
                trans = connection.begin()
                connection.execute(text(sql), params)
                trans.commit()
            return True
        except Exception as e:
            print(f"Error occurred while executing the query: {e}")
            return False
    
    