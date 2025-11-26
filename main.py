from config import DBConfig
from database import MySQLClient
from repository import StudentRepository
from analytics import StudentAnalytics

def main():
    config = DBConfig()
    client = MySQLClient(config)
    repository = StudentRepository(client)
    analytics = StudentAnalytics(repository = repository)


    print("Step 1: Fetching data...")
    raw_df = repository.fetch_all_students()

    if raw_df.empty:
        print("\nFailed to fetch data or database is empty. Exiting.")
        return

   
    print("\n--- Initial Data Inspection ---")
    print(raw_df.info())
    print("\n--- Missing Value Counts ---")
    print(raw_df.isna().sum())

  
    print("\nStep 2: Running data analysis...")
   
    final_report_df = analytics.run_full_analysis(raw_df)

  
    print("\n--- Analysis Complete. Final Report Head: ---")
    print(final_report_df.head())
    
    output_filename = 'student_report.csv'
    final_report_df.to_csv(output_filename, index=False)
    print(f"\n--- Pipeline Finished. Report saved to {output_filename} ---")

if __name__ == "__main__":
    main()