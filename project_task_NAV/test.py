from project import (
    register_user,
    login,
    assign_teacher_to_student,
    update_student,
    delete_student,
    get_teachers_for_student,
    logs,
    list_all_students,
    get_teachers_for_student
)

    # Register users
# register_user("student", "reshik", "reshik.doe@example.com", "hik@123")
# register_user("teacher", "Dr. Sushmitha", "sushmitha@example.com", "sushu@123")

# Login users
# login("student", "ashik.doe@example.com", "ashik@123")
# login("teacher", "soni@example.com", "somni@123")


# Assign teacher to student
# assign_teacher_to_student(7, 5)

# Update a student
# update_student(1, "Ashik", "ashik@example.com", "new@123")

# Delete a student
# delete_student(3)

#Get teachers assigned to a student
get_teachers_for_student(7)

logs()

list_all_students()

