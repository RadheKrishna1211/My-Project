import sqlite3
from class_representations.teacher import Teacher
DBNAME = 'inclusive_play_database.db'

# Function to create the  tables if it doesn't exist
def create_tables():
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    #cursor.execute('''INSERT INTO tbl_student_results(student_id, exercise_id, exercise_details_id, answer) VALUES (1,1,1,"How are you?")''')
    #cursor.execute('''INSERT INTO tbl_student_results(student_id, exercise_id, exercise_details_id, answer) VALUES (1,1,2,"Fine I am")''')
    #connection.commit()
    #################### TEACHER TABLE ########################################

    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_teacher_master (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    user_name VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL)''')
    connection.commit()

    #################### STUDENT TABLE ########################################
    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_student_master
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             first_name VARCHAR(50) NOT NULL,
                             last_name VARCHAR(50) NOT NULL,
                             user_name VARCHAR(50) UNIQUE NOT NULL,
                             password VARCHAR(50) NOT NULL,
                             teacher_id INTEGER,
                             FOREIGN KEY(teacher_id) REFERENCES tbl_teacher_master(id))''')
    connection.commit()

    #################### EXERCISE MASTER TABLE ###############################
    #cursor.execute('''DROP TABLE tbl_exercise_master''')
    #connection.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_exercise_master(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   exercise_name VARCHAR(100) UNIQUE NOT NULL,
                   category VARCHAR(100) NOT NULL,
                   exercise_description TEXT,
                   teacher_id INTEGER NOT NULL,
                   FOREIGN KEY(teacher_id) REFERENCES tbl_teacher_master(id))''')
    connection.commit()

    #################### EXERCISE DETAILS TABLE ###############################
    #cursor.execute('''DROP TABLE tbl_quizzes_details''')
    #connection.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_quizzes_details(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   question_number INTEGER NOT NULL,
                   game1_word VARCHAR(6) NULL,
                   game2_sentence VARCHAR(100) NULL,
                   game3_question TEXT NULL,
                   game3_option1 VARCHAR(100) NULL,
                   game3_option2 VARCHAR(100) NULL,
                   game3_option3 VARCHAR(100) NULL,
                   game3_option4 VARCHAR(100) NULL,
                   game3_answer_option INTEGER NULL,
                   game4_option1_image_path TEXT NULL,
                   game4_option2_image_path TEXT NULL,
                   game4_option3_image_path TEXT NULL,
                   game4_option4_image_path TEXT NULL,
                   game4_answer_option TEXT NULL,
                   exercise_id INTEGER NOT NULL,
                   teacher_id INTEGER NOT NULL,
                   FOREIGN KEY(exercise_id) REFERENCES tbl_exercise_master(id),
                   FOREIGN KEY(teacher_id) REFERENCES tbl_teacher_master(id))''')
    connection.commit()

#assign execrcise 
    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_assign_exercise(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   exercise_id INTEGER NOT NULL,
                   student_id INTEGER NOT NULL,
                   FOREIGN KEY(student_id) REFERENCES tbl_student_master(id),
                   FOREIGN KEY(exercise_id) REFERENCES tbl_exercise_master(id))''')
    connection.commit()

#results
    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_student_results(
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					student_id INTEGER NOT NULL,
                    teacher_id INTEGER NOT NULL,
                    exercise_id INTEGER NOT NULL,
					exercise_details_id INTEGER NOT NULL,
                    question_number INTEGER NOT NULL,
					answer VARCHAR(100),
                    actual_answer VARCHAR(100),
					FOREIGN KEY(student_id) REFERENCES tbl_student_master(id),
                    FOREIGN KEY(exercise_id) REFERENCES tbl_exercise_master(id),
                    FOREIGN KEY(exercise_details_id) REFERENCES tbl_quizzes_details(id))''')
    connection.commit()
    connection.close()

###################################################TEACHER MASTER TABLE QUERIES########################################
def insert_teacher(teacher):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("INSERT INTO tbl_teacher_master(first_name, last_name, email, user_name, password) VALUES (?,?,?,?,?)",
                             (teacher.first_name,teacher.last_name, teacher.email, teacher.user_name, teacher.password))
    connection.commit()
    connection.close()

def get_teacher_id(user_name):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_teacher_master WHERE user_name=?",(user_name,))
        result = cursor.fetchone()
        
        if not result:
            result_ret=False
        else:
            result_ret = result[0]
    connection.close()
    return result_ret

def check_teacher_user_exists(user_name):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_teacher_master WHERE user_name=?",(user_name,))
   
        result = cursor.fetchall()
        if not result:
            result=False
    connection.close()
    return True

def check_teacher_user_password_match(user_name, password):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_teacher_master WHERE user_name=? and password=?",(user_name, password ))
        result = cursor.fetchall()
        if not result:
            result = False
    connection.close()
    return result

def get_teacher_user_names():
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT user_name FROM tbl_teacher_master")
        result = cursor.fetchall()
        if not result:
            result=False
    connection.close()
    return result

###################################################STUDENT MASTER TABLE QUERIES########################################
def insert_student(student):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("INSERT INTO tbl_student_master(first_name, last_name, user_name, password,teacher_id)  VALUES (?,?,?,?,?)",
                             (student.first_name,student.last_name, student.user_name, student.password,student.teacher_id))
    connection.commit()
    connection.close()

def check_student_exists(user_name, teacher_id):
    print("inside db check student exists...",user_name, teacher_id)
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_student_master WHERE user_name=? and teacher_id=?",(user_name,teacher_id))
   
        result = cursor.fetchall()
        if not result:
            result=False
    connection.close()
    return result


def edit_delete_student(teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT first_name,last_name,user_name FROM tbl_student_master WHERE teacher_id=?",(teacher_id,))
    tbl_student_master = cursor.fetchall()
    connection.close()
    return tbl_student_master

def delete_student(user_name, teacher_id):
    print("inside delete student in db")
    print(user_name)
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_student_master WHERE user_name=? and teacher_id=?",(user_name,teacher_id))
    connection.commit()
    connection.close()

def update_student(student_object):
    print("inside update student in db")
    print(student_object.first_name,student_object.last_name,student_object.user_name,student_object.password)
  
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()  
    sql_update_query = """Update tbl_student_master set first_name =?, last_name =?,  password =? where user_name =? and teacher_id=?"""
    input_data = (student_object.first_name, student_object.last_name, student_object.password, student_object.user_name, student_object.teacher_id)
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    connection.close()

def check_student_password_match(user_name, password, teacher_id):
    print("inside check student password match")
    print(user_name,password,teacher_id)
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_student_master WHERE user_name=? and password=? and teacher_id=?",(user_name, password, teacher_id))
        result = cursor.fetchall()
        print(result)
        if not result:
            result = False
    connection.close()
    return result

def get_student_id(student_user_name,teacher_id):
    print("inside db get student id")
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tbl_student_master WHERE user_name=? and teacher_id=?",(student_user_name, teacher_id,))

    student_row = cursor.fetchone()
    print("student row",student_row)
    connection.close()
    if student_row == False:
        print("inside db get student id: returned false")
        return False
    else:
        print("inside db get student id: returned",student_row[0])
        return student_row[0]


###################################################EXERCISE MASTER TABLE QUERIES########################################
def insert_exercise(exercise):
    print("insert exercise",exercise.exercise_name,exercise.category,exercise.exercise_description)
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("INSERT INTO tbl_exercise_master(exercise_name, category, exercise_description,teacher_id)  VALUES (?,?,?,?)",
                             (exercise.exercise_name,exercise.category, exercise.exercise_description,exercise.teacher_id))
    connection.commit()
    connection.close()

def check_exercise_exists(exercise_name, teacher_id):
    print("inside check exercise exists", exercise_name,teacher_id)
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_exercise_master WHERE exercise_name=? and teacher_id=?",(exercise_name,teacher_id))
   
        result = cursor.fetchall()
        if not result:
            result=False
    connection.close()
    return result
   
def get_exercise_id(exercise_name, teacher_id):
    print("inside db get exercise id")
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tbl_exercise_master WHERE exercise_name=? and teacher_id=?",(exercise_name, teacher_id,))
    exercise_row = cursor.fetchone()
    connection.close()
    if exercise_row == False:
        print("inside db get exercise id: returned false")
        return False
    else:
        print("inside db get exercise id: returned",exercise_row[0])
        return exercise_row[0]

def get_exercise_name_for_id(exercise_id,teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tbl_exercise_master WHERE teacher_id=? and id=?",(teacher_id, exercise_id))
    exercise_row = cursor.fetchone()
    connection.close()
    return exercise_row[1]

def get_exercise_names(teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT exercise_name FROM tbl_exercise_master WHERE teacher_id=?",(teacher_id,))
    exercise_names = cursor.fetchall()
    print(" inside get exercise name",exercise_names)
    ex_list=[]
    for i in exercise_names:
        ex_list.append("".join(i))
    print("ex_list",ex_list)
    connection.close()
    return ex_list

def get_exercise_name_category(exercise_name,teacher_id):
    print("inside db get ex name category",exercise_name,teacher_id)
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT exercise_name ,category FROM tbl_exercise_master WHERE exercise_name=? and teacher_id=?",(exercise_name,teacher_id))
    exercise_names = cursor.fetchall()
    print("exercise names fetched for category in db",exercise_names)
    connection.close()
    print("inside db exercise names returned get ex name cat",exercise_names)
    return exercise_names

def get_exercise_for_category(category, teacher_id):
    print("category: in db", category)
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT exercise_name FROM tbl_exercise_master WHERE category=? and teacher_id=?",(category,teacher_id))
    exercises = cursor.fetchall()
    connection.close()
    ex_list=[]
    for i in exercises:
        ex_list.append("".join(i))
    print("ex_list",ex_list)
    return ex_list


def edit_delete_exercise(user_name):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT exercise_name,category,exercise_description FROM tbl_exercise_master WHERE teacher_id=?",(user_name,))
    exercises = cursor.fetchall()
    connection.close()
    return exercises

def update_exercise(exercise_id,category,exercise_description,teacher_id):
    print("inside update exercise in db", exercise_id,category,exercise_description,teacher_id)  
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()  
    sql_update_query = """Update tbl_exercise_master set category=?,  exercise_description =? where id =? and teacher_id=?"""
    input_data = (category, exercise_description,exercise_id, teacher_id)
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    connection.close()

def delete_exercise(exercise_id, teacher_id):
    print("inside delete exercise in db")
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_exercise_master WHERE id=? and teacher_id=?",(exercise_id,teacher_id))
    connection.commit()
    connection.close()



###########################################EXERCISE DETAILS TABLE QUERIES##################################################
############GAME 1 #################################################################

def insert_word_question(exercise_id,question_number, word, teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    
    with connection:
        cursor.execute("INSERT INTO tbl_quizzes_details(exercise_id, question_number, game1_word, teacher_id) VALUES (?,?,?,?)",
                             (exercise_id,question_number,word, teacher_id))
    
    connection.commit()
    connection.close()


def edit_delete_question_game1(exercise_id,teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT question_number,game1_word FROM tbl_quizzes_details WHERE teacher_id=? and exercise_id=?",(teacher_id,exercise_id))
    questions = cursor.fetchall()
    connection.close()
    return questions

def update_question_game1(exercise_id,question_number,word,teacher_id):
    print("inside update game1 questions in db")  
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()  
    sql_update_query = """Update tbl_quizzes_details set game1_word=? where exercise_id =? and teacher_id=? and question_number=?"""
    input_data = (word,exercise_id, teacher_id,question_number)
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    connection.close()

def check_question_game1_exists(exercise_id, teacher_id,question_number):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_quizzes_details WHERE exercise_id=? and teacher_id=? and question_number=?",(exercise_id,teacher_id,question_number))  
        result = cursor.fetchone()
        if not result:
            result=False
    connection.close()
    return result

def delete_question_game1(question_number ,exercise_id,teacher_id):
    print("inside delete word in db")
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_quizzes_details WHERE question_number=? and exercise_id=? and teacher_id=?",(question_number,exercise_id,teacher_id))
    connection.commit()
    connection.close()


############GAME 2 #################################################################
def insert_sentence_question(exercise_id, question_number, sentence, teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    
    with connection:
        cursor.execute("INSERT INTO tbl_quizzes_details(exercise_id, question_number, game2_sentence, teacher_id) VALUES (?,?,?,?)",
                             (exercise_id,question_number,sentence, teacher_id))
    connection.commit()
    connection.close()

def edit_delete_question_game2(exercise_id,teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT question_number,game2_sentence FROM tbl_quizzes_details WHERE teacher_id=? and exercise_id=?",(teacher_id,exercise_id))
    questions = cursor.fetchall()
    connection.close()
    return questions

def update_question_game2(exercise_id,question_number,sentence,teacher_id):
    print("inside update game2 questions in db")  
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()  
    sql_update_query = """Update tbl_quizzes_details set game2_sentence=? where exercise_id =? and teacher_id=? and question_number=?"""
    input_data = (sentence,exercise_id, teacher_id,question_number)
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    connection.close()

def check_question_game2_exists(exercise_id, teacher_id, question_number):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_quizzes_details WHERE exercise_id=? and teacher_id=? and question_number=?",(exercise_id,teacher_id,question_number))  
        result = cursor.fetchone()
        if not result:
            result=False
    connection.close()
    return result

def delete_question_game2(question_number ,exercise_id,teacher_id):
    print("inside delete questions in db")
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_quizzes_details WHERE question_number=? and exercise_id=? and teacher_id=?",(question_number,exercise_id,teacher_id))
    connection.commit()
    connection.close()


############GAME 3 #################################################################  
def insert_objective_type_question(exercise_id, question_number, obj_question, option1, option2, option3, option4, answer, teacher_id):

    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    
    with connection:
        cursor.execute("INSERT INTO tbl_quizzes_details(exercise_id, question_number, game3_question, game3_option1, game3_option2,game3_option3, game3_option4, game3_answer_option, teacher_id) VALUES (?,?,?,?,?,?,?,?,?)",
                             (exercise_id, question_number, obj_question, option1, option2, option3, option4, answer, teacher_id))
    
    connection.commit()
    connection.close()


def edit_delete_question_game3(exercise_id,teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    print("inside db editdeletegame3 exid and teacher id", exercise_id, teacher_id)
    cursor.execute("SELECT question_number, game3_question, game3_option1, game3_option2, game3_option3, game3_option4, game3_answer_option FROM tbl_quizzes_details WHERE teacher_id=? and exercise_id=?",(teacher_id,exercise_id))
    questions = cursor.fetchall()
    print("inside db editdeletegame3ques ", questions)
    connection.close()
    return questions
                  

def update_question_game3(exercise_id,question_number, obj_question, option1, option2, option3, option4,answer_option, teacher_id):
    print("inside update game1 questions in db")  
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()  
    sql_update_query = """Update tbl_quizzes_details set game3_question=?, game3_option1=?, game3_option2=?, game3_option3=?, game3_option4=?, game3_answer_option=? where exercise_id =? and teacher_id=? and question_number=?"""
    input_data = (obj_question, option1, option2, option3, option4, answer_option, exercise_id, teacher_id, question_number)
    cursor.execute(sql_update_query, input_data),
    connection.commit()
    connection.close()


def check_question_game3_exists(exercise_id, teacher_id,question_number):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_quizzes_details WHERE exercise_id=? and teacher_id=? and question_number=?",(exercise_id,teacher_id,question_number))  
        result = cursor.fetchall()
        if not result:
            result=False
    connection.close()
    return result

def delete_question_game3(question_number ,exercise_id,teacher_id):
    print("inside delete word in db")
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_quizzes_details WHERE question_number=? and exercise_id=? and teacher_id=?",(question_number,exercise_id,teacher_id))
    connection.commit()
    connection.close()

############GAME 4 #################################################################

def insert_odd_one_out_question(exercise_id, question_number,image_paths,answer,teacher_id):
    
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    try:
        with connection:
            cursor.execute("INSERT INTO tbl_quizzes_details(exercise_id,question_number, game4_option1_image_path, game4_option2_image_path, game4_option3_image_path, game4_option4_image_path,game4_answer_option, teacher_id) VALUES (?,?,?,?,?,?,?,?)",
                             (exercise_id,question_number,image_paths[0],image_paths[1],image_paths[2],image_paths[3],answer,teacher_id))
    except connection.Error as e:

        print("Error: %s" % e.args[0])
    
    connection.commit()
    connection.close()

def edit_delete_question_game4(exercise_id,teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT question_number, game4_answer_option, game4_option1_image_path, game4_option2_image_path, game4_option3_image_path, game4_option4_image_path FROM tbl_quizzes_details WHERE teacher_id=? and exercise_id=?",(teacher_id,exercise_id))
    #cursor.execute("SELECT question_number, game4_option1_image_path,  game4_answer_option FROM tbl_quizzes_details WHERE teacher_id=? and exercise_id=?",(teacher_id,exercise_id))
    questions = cursor.fetchall()
    connection.close()
    return questions
                  

def update_question_game4(exercise_id,question_number, image_paths, answer_option,  teacher_id):
    print("inside update game4 questions in db")  
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()  
    sql_update_query = """Update tbl_quizzes_details set game4_option1_image_path=?, game4_option2_image_path=?, game4_option3_image_path=?, game4_option4_image_path=?,game4_answer_option=? where exercise_id =? and teacher_id=? and question_number=?"""
    input_data = (image_paths[0], image_paths[1],image_paths[2],image_paths[3],answer_option, exercise_id, teacher_id, question_number)
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    connection.close() 


def check_question_game4_exists(exercise_id, teacher_id,question_number):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_quizzes_details WHERE exercise_id=? and teacher_id=? and question_number=?",(exercise_id,teacher_id,question_number))  
        result = cursor.fetchall()
        if not result:
            result=False
    connection.close()
    return result

def delete_question_game4(question_number ,exercise_id,teacher_id):
    print("inside delete word in db")
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_quizzes_details WHERE question_number=? and exercise_id=? and teacher_id=?",(question_number,exercise_id,teacher_id))
    connection.commit()
    connection.close()

def delete_all_game4():
    
    print("inside delete word in db")
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_quizzes_details WHERE  exercise_id=4 and teacher_id=1")
    connection.commit()
    connection.close()
###### FOR ALL GAMES #################################################################
def get_last_question_number(exercise_id, teacher_id):
    connection= sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("select max(question_number) from tbl_quizzes_details WHERE exercise_id=? and teacher_id=?",(exercise_id,teacher_id))
    question_count = cursor.fetchone()
    connection.close()
    return question_count

#################### FOR ASSIGN EXERCICES ############################################
def get_unassigned_student_list_for_exercise(exercise_id,teacher_id):
    print(teacher_id)
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    cursor.execute("SELECT user_name FROM tbl_student_master WHERE teacher_id=?", (teacher_id,))
    students = cursor.fetchall()
    connection.close()
    print("inside database assign",students)
    student_list=[]
    for i in students:
        student_list.append("".join(i))
    print("student_list",student_list)
    return student_list

def insert_assign_quiz(exercise_id,student_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_assign_exercise WHERE exercise_id=? AND student_id=?",(exercise_id,student_id))
        result=cursor.fetchone()
        flag = 0
        if result == None:
            cursor.execute("INSERT INTO tbl_assign_exercise(exercise_id,student_id) VALUES (?,?)",
                             (exercise_id,student_id))
            flag = 1
    connection.commit()
    connection.close()
    return(flag)

###################### For UNASSIGN EXERCISE ################################
def unassign_quiz_exercise(exercise_id,student_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_assign_exercise WHERE exercise_id=? AND student_id=?", (exercise_id,student_id))
        result = cursor.fetchone()
        flag=0
        if result!=None:
            cursor.execute("DELETE FROM tbl_assign_exercise WHERE exercise_id=? AND student_id=?", (exercise_id,student_id))
            print("Quiz unassigned successfully.")
            flag=1
    connection.commit()
    connection.close()
    return(flag)


####################### Student Result ################################

def get_quizz_details(student_id,exercise_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_student_results WHERE exercise_id=? AND student_id=?",(exercise_id,student_id))
        result=cursor.fetchall()
    connection.close()
    return(result)

def get_answers(student_id,exercise_id, teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("select * from tbl_student_results where student_id=? and exercise_id=? and teacher_id=?", (student_id, exercise_id,teacher_id))
        #cursor.execute("SELECT tq.question_number,tq.game2_sentence  ,sr.answer FROM tbl_quizzes_details AS tq, tbl_student_results As sr  WHERE  tq.id=sr.exercise_details_id AND sr.student_id=? AND sr.exercise_id=?" ,(student_id,exercise_id))
        result=cursor.fetchall()
    connection.close()
    print("get answers db game2", result)
    return(result)

""" 
def get_answers_for_game1(student_id,exercise_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT tq.question_number,tq.game1_word  ,sr.answer FROM tbl_quizzes_details AS tq, tbl_student_results As sr  WHERE  tq.id=sr.exercise_details.id AND sr.student_id=? AND sr.exercise_id=?" ,(student_id,exercise_id))
        result=cursor.fetchall()
    connection.close()
    return(result)

def get_answers_for_game3(student_id,exercise_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT tq.question_number,tq.game3_question,tq.game3_answer_option  ,sr.answer FROM tbl_quizzes_details AS tq, tbl_student_results As sr  WHERE  tq.id=sr.exercise_details.id AND sr.student_id=? AND sr.exercise_id=?" ,(student_id,exercise_id))
        result=cursor.fetchall()
    connection.close()
    return(result)

def get_answers_for_game4(student_id,exercise_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT tq.question_number,tq.game4_answer_option ,sr.answer FROM tbl_quizzes_details AS tq, tbl_student_results As sr  WHERE  tq.id=sr.exercise_details.id AND sr.student_id=? AND sr.exercise_id=?" ,(student_id,exercise_id))
        result=cursor.fetchall()
    connection.close()
    return(result)

 """
def get_exercise_list_for_student(student_id,category):
    print("INSIDE DB EX LIST...",student_id, category)
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT asn.exercise_id, em.exercise_name FROM tbl_assign_exercise as asn, tbl_exercise_master as em WHERE asn.exercise_id = em.id and student_id=? and em.category=?",(student_id,category))
        result=cursor.fetchall()
        print("RESULT....", result)
    connection.close()
    if result:
        ex_list=[]
        for i in result:
            #print("iiii", i)
            temp=[]
            for j in i:
                #print("jjj ", j)
                temp.append(j)
            ex_list.append(temp)
    else:
        ex_list = False
    connection.close()
    return ex_list

def get_all_quests():
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    #print("inside all quest...")
    with connection:
        cursor.execute("SELECT exercise_id,teacher_id FROM tbl_quizzes_details")
        result=cursor.fetchall()
        #print(result)
        #print("end all quest")
    connection.close()
    return result


def get_questions_for_game1_exercise(exercise_id,teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    print("inside quest game1...",exercise_id,teacher_id)
    with connection:
        cursor.execute("SELECT id, question_number, game1_word FROM tbl_quizzes_details WHERE exercise_id =? and teacher_id=?",(exercise_id,teacher_id))
        result=cursor.fetchall()
    connection.close()
    print("ins ques game1 db-result ",result)
    if result:
        question_list=[]
        for i in result:
            temp=[]
            for j in i:
                temp.append(j)
            question_list.append(temp)
    else:
        question_list = []
    connection.close()
    return question_list


def get_questions_for_game2_exercise(exercise_id,teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    print("inside quest game2...",exercise_id,teacher_id)
    with connection:
        cursor.execute("SELECT id, question_number, game2_sentence FROM tbl_quizzes_details WHERE exercise_id =? and teacher_id=?",(exercise_id,teacher_id))
        result=cursor.fetchall()
    connection.close()
    print("ins ques game2 db-result ",result)
    if result:
        question_list=[]
        for i in result:
            temp=[]
            for j in i:
                temp.append(j)
            question_list.append(temp)
    else:
        question_list = []
    connection.close()
    return question_list

def get_questions_for_game3_exercise(exercise_id,teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    print("inside quest game3...",exercise_id,teacher_id)
    with connection:
        cursor.execute("SELECT id, question_number, game3_question, game3_option1, game3_option2, game3_option3, game3_option4, game3_answer_option FROM tbl_quizzes_details WHERE exercise_id =? and teacher_id=?",(exercise_id,teacher_id))
        result=cursor.fetchall()
    connection.close()
    print("ins ques game3 db-result ",result)
    if result:
        question_list=[]
        for i in result:
            temp=[]
            for j in i:
                temp.append(j)
            question_list.append(temp)
    else:
        question_list = []
    connection.close()
    return question_list

def get_questions_for_game4_exercise(exercise_id,teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    print("inside quest game4...",exercise_id,teacher_id)
    with connection:
        cursor.execute("SELECT id, question_number, game4_option1_image_path,game4_option2_image_path,game4_option3_image_path,game4_option4_image_path, game4_answer_option FROM tbl_quizzes_details WHERE exercise_id =? and teacher_id=?",(exercise_id,teacher_id))
        result=cursor.fetchall()
    connection.close()
    print("ins ques game4 db-result ",result)
    if result:
        question_list=[]
        for i in result:
            temp=[]
            for j in i:
                temp.append(j)
            question_list.append(temp)
    else:
        question_list = []
    connection.close()
    return question_list



def insert_result_for_student(student_id,teacher_id,exercise_id,exercise_questions_id,question_number, answer, actual_answer):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("INSERT INTO tbl_student_results(student_id, teacher_id, exercise_id,exercise_details_id , question_number, answer, actual_answer) VALUES (?,?,?,?,?,?,?)",
                             (student_id,teacher_id,exercise_id,exercise_questions_id,question_number, answer, actual_answer))
    connection.commit()
    connection.close()

def delete_if_exists(student_id,teacher_id,exercise_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE FROM tbl_student_results WHERE student_id=? and teacher_id=? and exercise_id=?",(student_id,teacher_id,exercise_id))
    connection.commit()
    connection.close()

def get_teacher_details_for_profile(teacher_id):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT * FROM tbl_teacher_master WHERE id=?",(teacher_id,))
        result = cursor.fetchall()
        if not result:
            result=False
    connection.close()
    return result
   
def update_teacher_profile(first_name,last_name,email,teacher_id):
    
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()  
    sql_update_query = """Update tbl_teacher_master set first_name =?, last_name =?, email=? WHERE id=?"""
    input_data = (first_name, last_name, email, teacher_id)
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    connection.close()




