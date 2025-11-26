from database import MySQLClient

class StudentRepository:
    def __init__(self, client: MySQLClient):
        self.client = client
    
    def fetch_all_students(self):
        query = "SELECT * FROM students"
        return self.client.query_to_data_frame(query)
    
    def fetch_student_by_major(self, major: str):
        query = f"SELECT * FROM students WHERE major = '{major}"
        return self.client.query_to_data_frame(query)
    def fetch_by_gpa_range(self, min_gpa: float, max_gpa: float):
        query = f"SELECT * FROM students where gpa BETWEEN {min_gpa} AND {max_gpa}"
        return self.client.query_to_data_frame(query)
    def fetch_students_by_name(self, name: str):
        query = f"SELECT * FROM students WHERE name LIKE '%{name}%'"
        return self.client.query_to_data_frame(query)
    def count_all_students(self):
        query = "SELECT COUNT(*) AS student_count FROM students"
        df = self.client.query_to_data_frame(query)

        if not df.empty:
            return df.iloc[0, 0]
        return 0
    def add_student(self, student_id: str, first_name: str, last_name: str, dob: str, major: str, gpa: float) -> bool:
        query = """
        INSERT INTO students (student_id, first_name, last_name, dob, major, gpa)
        VALUES (:student_id, :first_name, :last_name, :dob, :major, :gpa)
        """
        params = {
            "student_id": student_id,
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob,
            "major": major,
            "gpa": gpa
        }
        return self.client.execute_query(query, params)
    def edit_student(self, student_id: str, first_name: str, last_name:str, dob: str, major: str, gpa: float) -> bool:
        query = """
        UPDATE students
        SET first_name = :first_name, last_name = :last_name, dob = :dob, major = :major, gpa = :gpa
        WHERE student_id = :student_id
        """
        params = {
            "student_id": student_id,
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob,
            "major": major,
            "gpa": gpa
        }
        return self.client.execute_query(query, params)
    def delete_student(self, student_id: str) -> bool:
        query = "DELETE FROM students WHERE student_id = :student_id"
        params = {"student_id": student_id}
        return self.client.execute_query(query, params)
    
