import tkinter as tk
from tkinter import messagebox
import pyttsx3
import scan_select_exercise as se
import database_code as db
import scan_select_category as ssc
import scan_selected_questions_display_game1 as sqdg1
import scan_selected_questions_display_game2 as sqdg2
import scan_selected_questions_display_game3 as sqdg3
import scan_selected_questions_display_game4 as sqdg4


HCOLOR = "yellow"
BCOLOR = "cyan4"
FCOLOR = "white"

class ScanSelectedExerciseDisplay:
    def __init__(self, master, header_frame, display_frame, actual_index, student_id, teacher_id, selected_exercise_name, selected_exercise_id, category):
        self.scan_list=[]
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.header_frame = header_frame
        self.display_frame=display_frame
        self.master = master
        self.actual_index =  actual_index
        self.exercise_id = selected_exercise_id
        self.exercise_name = selected_exercise_name
        self.category = category
        self.exercise_questions = self.get_questions(self.exercise_id,self.teacher_id)
        if len(self.exercise_questions) == 0:
            messagebox.showerror("Scan Section","No Questions in the exercise selected")
            ssc.ScanSelectCategory(self.master, self.student_id, self.teacher_id)
        else:
            result=[]
            if category == "Alphabet Scramble":
                sqdg1.ScanSelectedQuestionsDisplayGame1(master, header_frame, display_frame, student_id, teacher_id, selected_exercise_name, selected_exercise_id, category,self.exercise_questions,0 , result)
            elif self.category == "Sentence Builder":
                sqdg2.ScanSelectedQuestionsDisplayGame2(master, header_frame, display_frame, student_id, teacher_id, selected_exercise_name, selected_exercise_id, category,self.exercise_questions,0 , result)
            elif self.category == "Objective Type Questions":
                sqdg3.ScanSelectedQuestionsDisplayGame3(master, header_frame, display_frame, student_id, teacher_id, selected_exercise_name, selected_exercise_id, category,self.exercise_questions,0 , result)
            else:
                sqdg4.ScanSelectedQuestionsDisplayGame4(master, header_frame, display_frame, student_id, teacher_id, selected_exercise_name, selected_exercise_id, category,self.exercise_questions,0 , result)
    
    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    
    def get_questions(self,exercise_id, teacher_id):
        self.complete_questions_data = db.get_questions_for_exercise(exercise_id,teacher_id)
        self.questions_list = []
        if self.category == "Alphabet Scramble":
            print("AS")
            for row in self.complete_questions_data:
                temp = []
                temp.append(row[1])
                temp.append(row[2])
                self.questions_list.append(temp)
            print(self.questions_list)
        elif self.category == "Sentence Builder":
            print("SB")
            for row in self.complete_questions_data:
                temp = []
                temp.append(row[1])
                temp.append(row[3])
                self.questions_list.append(temp)
            print(self.questions_list)
        elif self.category == "Objective Type Questions":
            print("OT")
            for row in self.complete_questions_data:
                temp = []
                temp.append(row[1])
                temp.append(row[4])
                temp.append(row[5])
                temp.append(row[6])
                temp.append(row[7])
                temp.append(row[8])
                temp.append(row[9])
                self.questions_list.append(temp)
            print(self.questions_list)
        else:
            print("OOOI")
            for row in self.complete_questions_data:
                temp = []
                temp.append(row[1])
                temp.append(row[10])
                temp.append(row[11])
                temp.append(row[12])
                temp.append(row[13])
                temp.append(row[14])
                self.questions_list.append(temp)
            print(self.questions_list)
        return self.questions_list            

