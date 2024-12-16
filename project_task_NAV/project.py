import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# file is connected to PostgreSQL.

Student_db = "stud_management"
Teacher_db = "teacher_management"
Username = "postgres"
Password = "Midhun@123"
host = "localhost"
Port = "5432"

def connect_to_db(database):
    return psycopg2.connect(
        dbname=database, user=Username, password=Password, host=host, port=Port
    )
#========================================================================
def register_user(user_type, name, email, password):
    if user_type == "student":
        db = Student_db
        table = "students"
    elif user_type == "teacher":
        db = Teacher_db
        table = "teachers"
    else:
        raise ValueError("user type invalid")

    conn = connect_to_db(db)
    cursor = conn.cursor()
    try:
        query = f"INSERT INTO {table} (name, email, password) VALUES (%s, %s, %s) RETURNING *"
        cursor.execute(query, (name, email, password))
        conn.commit()
        print(f"{user_type.capitalize()} registered successfully.")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
#======================================================================
def login(user_type, email, password):
    if user_type == "student":
        db = Student_db
        table = "students"
    elif user_type == "teacher":
        db = Teacher_db
        table = "teachers"
    else:
        raise ValueError("user type invalid")

    conn = connect_to_db(db)
    cursor = conn.cursor()
    try:
        query = f"SELECT name FROM {table} WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        if user:
            print(f"Welcome {user[0]}!")
            log_sign_in(user[0], user_type)
        else:
            print("Invalid username/password")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
#================================================================
def log_sign_in(name, user_type):
    conn = connect_to_db(Teacher_db)
    cursor = conn.cursor()
    try:
        query = "INSERT INTO logs (user_name, user_type) VALUES (%s, %s)"
        cursor.execute(query, (name, user_type))
        conn.commit()
        print("Sign-in logged")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
#================================================================
def assign_teacher_to_student(student_id, teacher_id):
    conn = connect_to_db(Student_db)
    cursor = conn.cursor()
    try:
        query = "INSERT INTO student_teacher (student_id, teacher_id) VALUES (%s, %s)"
        cursor.execute(query, (student_id, teacher_id))
        conn.commit()
        print(f"Teacher {teacher_id} assigned to Student {student_id}.")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
#================================================================
def update_student(student_id, name, email, password):
    conn = connect_to_db(Student_db)
    cursor = conn.cursor()
    try:
        query = "UPDATE students SET name=%s, email=%s, password=%s WHERE id=%s"
        cursor.execute(query, (name, email, password, student_id))
        conn.commit()
        print("Student updated successfully.")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
#================================================================
def delete_student(student_id):
    conn = connect_to_db(Student_db)
    cursor = conn.cursor()
    try:
        query = "DELETE FROM students WHERE id=%s"
        cursor.execute(query, (student_id,))
        conn.commit()
        print("Student deleted successfully.")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

#================================================================
def list_all_students():
    conn = connect_to_db(Student_db)
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM students;"
        cursor.execute(query)
        students = cursor.fetchall()
        print("List of all students:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
#================================================================
def get_teachers_for_student(student_id):
    conn = connect_to_db(Student_db)
    cursor = conn.cursor()
    try:
        query = "SELECT teacher_name, teacher_email FROM teachers_for_students WHERE student_id = %s;"
        cursor.execute(query, (student_id,))
        teachers = cursor.fetchall()
        print(f"Teachers assigned to student ID {student_id}:")
        for teacher in teachers:
            print(f"Name: {teacher[0]}, Email: {teacher[1]}")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


#================================================================
def logs():
    conn = connect_to_db(Teacher_db)
    cursor = conn.cursor()
    try:
        query = "SELECT user_name, user_type, logged_in_time FROM logs;"
        cursor.execute(query)
        log_entries = cursor.fetchall()
        
        print("Logs:")
        for entry in log_entries:
            print(f"Username: {entry[0]}, User Type: {entry[1]}, Logged In Time: {entry[2]}")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

#================================================================
def get_teachers_for_student(student_id):
    conn = connect_to_db(Student_db)
    cursor = conn.cursor()
    try:
        query_student_teacher = "SELECT teacher_id FROM student_teacher WHERE student_id = %s"
        cursor.execute(query_student_teacher, (student_id,))
        teacher_ids = cursor.fetchall()
        if not teacher_ids:
            print("No teachers assigned to this students")
            return
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return
    finally:
        cursor.close()
        conn.close()

    conn_teacher = connect_to_db(Teacher_db)
    cursor_teacher = conn_teacher.cursor()
    try:
        query_teachers = "SELECT name FROM teachers WHERE id = ANY(%s)"
        teacher_id_list = [t[0] for t in teacher_ids]
        cursor_teacher.execute(query_teachers, (teacher_id_list,))
        teachers = cursor_teacher.fetchall()
        if teachers:
            print("Teachers assigned to the students r:")
            for teacher in teachers:
                print(teacher[0])
        else:
            print("No teacher records")
    except psycopg2.Error as e:
        print(f"Errorr: {e}")
    finally:
        cursor_teacher.close()
        conn_teacher.close()


