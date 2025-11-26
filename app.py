import streamlit as st
import pandas as pd


from config import DBConfig
from database import MySQLClient
from repository import StudentRepository
from analytics import StudentAnalytics

st.set_page_config(page_title= "Data of student analyzed", layout = "wide")
st.title("Student Analytics")



@st.cache_resource

def init_system():

    try:
        config = DBConfig()
        client = MySQLClient(config)
        repo = StudentRepository(client)
        analytics = StudentAnalytics(repo)
        return repo, analytics
    except Exception as e:
        st.error(f"Failed to connect to Database: {e}")
        return None, None

repo, analytics = init_system()

if not repo or not analytics:
    st.stop()

with st.sidebar:
    st.header("Pipeline Control")
    if st.button("Refresh data from DB"):
        st.cache_data.clear()
        st.rerun()

tab_view, tab_report = st.tabs(["Raw Data", "Analytics Report"])

with tab_view:
    st.subheader("Current Database")

    try:
        raw_df = repo.fetch_all_students()
        if raw_df.empty:
            st.warning("No data founded")
        else:
            col1, col2 = st.columns(2)
            col1.metric("Total students", len(raw_df))
            col1.metric("Columns", len(raw_df.columns))
        
        st.dataframe(raw_df, use_container_width= True)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

with tab_report:
    st.subheader("Processed Dataset")
    st.write("Perform imputating, BMI/Age calculation, Z-score calculation and Outlier detection")
    
    if st.button("Run analysis", type = "primary"):
        with st.spinner("Processing..."):
            try:
                df_input = repo.fetch_all_students()
                if df_input.empty:
                    st.error("Cannot run analysis")
                else:
                    df_processed = analytics.run_full_analysis(df_input)

                    if hasattr(analytics, 'get_summary_by_major'):
                        summary_df = analytics.get_summary_by_major(df_processed)
                        top_k_df = analytics.get_top_k_student(df_processed)
                    else: 
                        st.warning(f"Function not found")
                        summary_df = None
                        top_k_df = None

                    st.success("Pipeline finished successfully")

                    if summary_df is not None:
                        st.write("Summary by Major")
                        st.dataframe(summary_df, hide_index = True)

                    if top_k_df is not None:
                        st.write("Top student per major")
                        st.dataframe(top_k_df, hide_index = True)
                    st.write("Processed data")
                    st.dataframe(df_processed)

                    csv = df_processed.to_csv(index= False).encode('utf-8')
                    st.download_button(
                        label = "Download CSV file",
                        data = csv,
                        file_name= "final_student_report.csv",
                        mime = "text/csv"
                    )
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.exception(e)
