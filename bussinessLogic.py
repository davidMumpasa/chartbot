import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='DavidEbula1999',
    database='lms'
)
cursor = conn.cursor()


def fetch_user_login(user_email):
    query = f"SELECT user_id FROM user WHERE email = '{user_email}'"
    user_id = execute_query(query)
    if user_id:
        return user_id[0][0]
    else:
        return None


def fetch_user_data(user_email):
    query = f"SELECT * FROM user WHERE email = '{user_email}'"
    return execute_query(query)


def fetch_user_quizzes(user_email):
    user_id = fetch_user_login(user_email)
    query = f"SELECT * FROM quizz_has_user WHERE user_id = '{user_id}'"
    return execute_query(query)


def fetch_all_user_quizzes():
    query = "SELECT * FROM quizz_has_user"
    return execute_query(query)


def fetch_all_course_users():
    query = "SELECT * FROM user_has_course"
    return execute_query(query)


def fetch_quizzes():
    query = "SELECT * FROM quizz"
    return execute_query(query)


def fetch_user_badges(user_email):
    user_id = fetch_user_login(user_email)
    query = f"SELECT * FROM badge WHERE user_id = '{user_id}'"
    return execute_query(query)


def fetch_badges():
    query = "SELECT * FROM badge"
    return execute_query(query)


def fetch_courses():
    query = "SELECT * FROM course"
    return execute_query(query)


def fetch_users():
    query = "SELECT * FROM user"
    return execute_query(query)


def fetch_user_has_course():
    query = "SELECT * FROM user_has_course"
    return execute_query(query)


def execute_query(query):
    cursor.execute(query)
    return cursor.fetchall()


def convert_data_to_documents(users, user_quizzies, quizzies, courses, courseUser, badges):
    combined_content = ""

    for user in users:
        user_content = f"User ID: {user[0]}\n" \
                       f"User First Name: {user[1]}\n" \
                       f"User Last Name: {user[2]}\n" \
                       f"User Email: {user[3]}\n" \
                       f"User Avatar: {user[4]}\n" \
                       f"User Bio: {user[5]}\n" \
                       f"User Created At: {user[6]}\n" \
                       f"User Credits: {user[7]}\n" \
                       f"User Deactivation Date: {user[8]}\n" \
                       f"User Language: {user[9]}\n" \
                       f"User Updated At: {user[10]}\n" \
                       f"User Level: {user[11]}\n" \
                       f"User Points: {user[12]}\n" \
                       f"User Restrict Email: {user[13]}\n" \
                       f"User Status: {user[14]}\n" \
                       f"User Timezone: {user[15]}\n" \
                       f"User Type: {user[16]}\n"
        combined_content += user_content + "\n\n"

    for badge in badges:
        badge_content = f"Badge ID: {badge[0]}\n" \
                        f"User ID: {badge[1]}\n" \
                        f"Badge Set ID: {badge[2]}\n" \
                        f"Criteria: {badge[3]}\n" \
                        f"Image URL: {badge[4]}\n" \
                        f"Issued On: {badge[5]}\n" \
                        f"Issued On Timestamp: {badge[6]}\n" \
                        f"Name: {badge[7]}\n" \
                        f"Type: {badge[8]}\n"
        combined_content += badge_content + "\n\n"

    for quizz_user in user_quizzies:
        quizz_user_content = f"Quiz Name: {quizz_user[0]}\n" \
                             f"User ID: {quizz_user[1]}\n" \
                             f"Score: {quizz_user[2]}\n" \
                             f"Status: {quizz_user[3]}\n" \
                             f"Total Max: {quizz_user[4]}\n" \
                             f"Course ID: {quizz_user[5]}\n" \
                             f"Created At: {quizz_user[6]}\n"  # Add the new field here
        # ... (Add all the remaining quizzUser fields here)
        combined_content += quizz_user_content + "\n\n"

    # Add quiz data to the combined content
    for quiz in quizzies:
        quiz_content = f"Quiz ID: {quiz[0]}\n" \
                       f"Quiz Name: {quiz[1]}\n" \
                       f"Quiz Created At: {quiz[2]}\n"  # Add the new field here
        # ... (Add all the remaining quiz fields here)
        combined_content += quiz_content + "\n\n"

    # Add courseUser data to the combined content
    for course_user in courseUser:
        course_user_content = f"User ID: {course_user[0]}\n" \
                              f"Course ID: {course_user[1]}\n" \
            # ... (Add all the courseUser fields here)
        combined_content += course_user_content + "\n\n"

    for course in courses:
        course_content = f"Course ID: {course[0]}\n" \
                         f"Course Name: {course[1]}\n" \
                         f"Course Avatar: {course[2]}\n" \
                         f"Course Big Avatar: {course[3]}\n" \
                         f"Course Code: {course[4]}\n" \
                         f"Course Creation Date: {course[5]}\n" \
                         f"Course Creator ID: {course[6]}\n" \
                         f"Course Description: {course[7]}\n" \
                         f"Course Expiration Datetime: {course[8]}\n" \
                         f"Course Hide from Catalog: {course[9]}\n" \
                         f"Course Last Update On: {course[10]}\n" \
                         f"Course Level: {course[11]}\n" \
                         f"Course Price: {course[12]}\n" \
                         f"Course Shared: {course[13]}\n" \
                         f"Course Shared URL: {course[14]}\n" \
                         f"Course Start Datetime: {course[15]}\n" \
                         f"Course Status: {course[16]}\n" \
                         f"Course Time Limit: {course[17]}\n"
        combined_content += course_content + "\n\n"

    return combined_content
