import pandas as pd
from datetime import datetime
from repository import StudentRepository
class StudentAnalytics:
    def __init__ (self, repository: StudentRepository, reference_date: str = '2025-10-01'):
        self.repository = repository
        self.reference_date = pd.to_datetime(reference_date)
    
    def run_full_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        df_processed = df.copy()
       
        df_processed = self.impute_missing(df_processed)
        df_processed = self.add_bmi(df_processed)
        df_processed = self.calculate_age(df_processed)
        df_processed = self.flag_outliers(df_processed)
        df_processed = self.calculate_zscores(df_processed)

        return df_processed

   
    def impute_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df['height_cm'] = df.groupby('gender')['height_cm'].transform(lambda x: x.fillna(x.median()))
        df['weight_kg'] = df.groupby('gender')['weight_kg'].transform(lambda x: x.fillna(x.median()))
        df['gpa'] = df.groupby('major')['gpa'].transform(lambda x: x.fillna(x.median()))
        return df
    
    def add_bmi(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df['height_m'] = df['height_cm'] / 100
        df['bmi'] = df['weight_kg'] / (df['height_m'] ** 2)
        return df
    
    def calculate_age(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df['dob'] = pd.to_datetime(df['dob'])
        time_delta = self.reference_date - df['dob']
        df['age'] = (time_delta.dt.days / 365.25)
        return df
    
    def calculate_zscores(self, df: pd.DataFrame, ) -> pd.DataFrame:
        col_to_score = ['gpa', 'credits', 'bmi', 'age']   

        for col in col_to_score:
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()

                if std > 0:
                     df[f'{col}_zscore'] = (df[col] - mean ) / std
        return df
    def flag_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        col_to_check = ['gpa', 'bmi']

        for col in col_to_check:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - (1.5 * IQR)
                upper_bound = Q3 + (1.5 * IQR)

                df[f'is{col}_outlier'] = (df[col] < lower_bound ) | (df[col] > upper_bound)
       
        return df

    def get_summary_by_major(self, df: pd.DataFrame):
        summary = df.groupby('major').agg({
            'student_id': 'count',
            'gpa': 'mean',
            'credit': 'mean',
            'bmi': 'mean',
        }).reset_index()
        summary.columns = ['major', 'n_students', 'mean_gpa', 'mean_credit', 'mean_bmi']
        summary.sort_values(by = 'mean_gpa', ascending= False)
        return summary
    
    def get_top_k_student(self, df = pd.DataFrame, k: int = 3):
        sorted_df = df. sort_values(
            by = ['major', 'gpa', 'credit'], 
            ascending= [ True, False, False])
        return sorted_df.groupby('major').head(k)

     