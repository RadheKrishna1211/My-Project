import tkinter as tk
from tkinter import messagebox
import pyttsx3
import scan_select_exercise as se
import database_code as db
import scan_select_category as ssc
import result_display as rd
from random import shuffle
import time 



HCOLOR = "yellow"
BCOLOR = "cyan4"
FCOLOR = "white"
TITLEFG = '#2D1BA6'
TITLEBG = '#ffffcc'

class ScanStudentResultPageGame4:
    def __init__(self, master, header_frame, display_frame, student_id, teacher_id, selected_exercise_name, category,exercise_questions, final_result ):
        
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.header_frame = header_frame
        self.display_frame=display_frame
        self.master = master
        self.exercise_name = selected_exercise_name
        self.exercise_questions = exercise_questions
        self.final_result = final_result      
        self.category = category
        self.score = 0

        self.calculate_score()
        print("score is", self.score)
        self.result_text = "You scored " + str(self.score) + " out of "+ str(len(self.exercise_questions))
        print("result string is ",self.result_text)
        self.voice_initializations()
        
        
        self.title = "Hey, Here is your Score!!"
        
        self.master.title("Inclusive Scan and Play Software")
        self.master.state('zoomed')#automatically expands window to full size
        
        self.master.configure(bg='cyan4')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        
        self.title_label = tk.Label(self.header_frame,  font=("Arial",30,"bold"),width=50, background=TITLEBG,fg=TITLEFG)
        self.title_label.grid(row=0, column = 0)
        
        self.title_label.configure(text=self.title)
        
        
        
        self.create_screen()
        #self.master.after(100, self.highlight_buttons) 

        self.master.bind('<Button-1>', self.on_mouse_click)
        self.master.after(1000, self.speak_text)

    def calculate_score(self):
        i=0
        print("in calculate score")
        print(self.final_result)
        for row in self.final_result:
            print("row", row)
            print("original", self.exercise_questions[i][6])
            if int(row) == int(self.exercise_questions[i][6]):
                self.score=self.score+1
            i=i+1

    def insert_result_data(self):
        db.delete_if_exists(self.student_id,self.teacher_id,self.exercise_id)
        i=0
        print("in insert result data")
        print(self.final_result)
        for row in self.final_result:
            print("row", str(row))
            db.insert_result_for_student(self.student_id,self.teacher_id,self.exercise_id,self.exercise_questions[i][0],self.exercise_questions[i][1],str(row), str(self.exercise_questions[i][6]))
            print("original", str(self.exercise_questions[i][6]))     
            i=i+1    

    def voice_initializations(self):
        self.engine = pyttsx3.init()
        self.engine. setProperty("rate",150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)#female voice
 
    def create_screen(self):
        self.exercise_label = tk.Label(self.display_frame,font=("Arial",20,"bold"), width=20, background=BCOLOR, fg=FCOLOR)
        self.exercise_label.grid(row=0,column=0)     
        self.exercise_label.configure(text="Exercise Name")
        print("exercise name in create screen",self.exercise_name)
        self.exercise_label_display = tk.Label(self.display_frame, font=("Arial",20,"bold"), width=20, background=BCOLOR, fg=FCOLOR)
        self.exercise_label_display.grid(row=0,column=1, pady=10)
        self.exercise_label_display.configure(text=self.exercise_name)
        
        self.result_label = tk.Label(self.display_frame,font=("Arial",20,"bold"),  width=20, background=BCOLOR, fg=FCOLOR)
        self.result_label.grid(row=1,column=0, pady = 50)     
        self.result_label.configure(text="Score: ")
        self.result_label_display = tk.Label(self.display_frame,font=("Arial",20,"bold"), width=20, background=BCOLOR, fg=FCOLOR)
        self.result_label_display.grid(row=1,column=1)
        self.result_label_display.configure(text=self.result_text)     
        self.message_label = tk.Label(self.display_frame,  font=("Arial",20,"bold"),width=50, background=TITLEBG,fg=TITLEFG)
        self.message_label.grid(row=2,column=0,columnspan=2,pady=50)     
        self.message_label.configure(text="Click to go back to Select Category!!")
        
    def speak_text(self):
        self.engine.say(self.result_text)
        self.engine.runAndWait()
        self.engine.say("Click to go back to Select Category!!")
        self.engine.runAndWait()  
   
    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def on_mouse_click(self,event):
       print("on mouse click")
       self.clear_frame(self.header_frame)
       self.clear_frame(self.display_frame)
       self.header_frame.destroy()
       self.display_frame.destroy()
       ssc.ScanSelectCategory(self.master, self.student_id,self.teacher_id)    
       ###############################################3
