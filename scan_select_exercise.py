import tkinter as tk
from tkinter import messagebox
import pyttsx3
import database_code as db
import scan_select_category as ssc
import scan_select_exercise as se
import scan_selected_questions_display_game1 as ssqg1
import scan_selected_questions_display_game2 as ssqg2
import scan_selected_questions_display_game3 as ssqg3
import scan_selected_questions_display_game4 as ssqg4

HCOLOR = "yellow"
BCOLOR = "cyan4"
FCOLOR = "white"

class ScanSelectExercise:
    def __init__(self, master, header_frame, display_frame, actual_index, student_id, teacher_id, category ):
    
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.header_frame = header_frame
        self.display_frame=display_frame
        self.master = master
        self.actual_index =  actual_index
        self.category = category
        print("ALL DATA IN SCAN EXERCISE", self.teacher_id,self.student_id,self.category)
        self.exercise_list = db.get_exercise_list_for_student(student_id,self.category)
        
        self.master = master
        
        self.scan_list = []
        if self.exercise_list == False:
            messagebox.showerror('student section', "There is no exercise assigned to you. Contact your teacher!")
            ssc.ScanSelectCategory(self.master, self.student_id, self.teacher_id)
        else:
            self.title = "Select the Exercise!!"
            for row in self.exercise_list:
                self.scan_list.append(row[1])

            self.master.title("Inclusive Scan and Play Software")
            self.master.state('zoomed')#automatically expands window to full size
        
            self.master.configure(bg='cyan4')
            self.master.rowconfigure(0, weight=1)
            self.master.columnconfigure(0, weight=1)

            self.header_frame=tk.Frame(self.master,background="cyan4")
            self.header_frame.grid()
            self.display_frame=tk.Frame(self.master,background="cyan4")
            self.display_frame.grid()
            self.title_label = tk.Label(self.header_frame,  font=("Arial",30,"bold"),width=50, background='#ffffcc',fg='#2D1BA6')
            self.title_label.grid(row=0, column = 0)
            
            self.title_label.configure(text=self.title)
        
            self.variable_initializations()

            
            self.voice_initializations()
            self.create_buttons()
            self.master.after(100, self.highlight_buttons) 

            self.master.bind('<Button-1>', self.on_mouse_click)

    def variable_initializations(self):
        self.highlight_flag = 1
        self.flag = 0
        self.label_widgets = []
        self.button_widgets = []
        self.counter = 0
        self.highlight_index = 0
        

    def voice_initializations(self):
        self.engine = pyttsx3.init()
        self.engine. setProperty("rate",150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)#female voice
 

    def create_buttons(self):
        for i in range(0,len(self.scan_list)): 
            
            self.surround_label = tk.Label(self.display_frame, height=300,width=300, background=BCOLOR)
            rowval = i//2
            colval = i%2
            self.surround_label.grid(row=rowval,column=colval,pady=5)     
            button = tk.Button(self.surround_label,height=5, font=("Arial",20,"bold"), width=30,background=BCOLOR,fg=FCOLOR)
            button.grid(row=rowval, column=colval, pady=10,padx=20)
            self.button_widgets.append(button)

            button.configure(text=self.scan_list[i])
            
            self.label_widgets.append(self.surround_label)
        self.dummy_header_label = tk.Label(self.display_frame,  font=("Arial",30,"bold"),width=30, background=BCOLOR,fg=BCOLOR)
        rowvalfinal = (len(self.scan_list)+1)//2
        self.dummy_header_label.grid(row=rowvalfinal, column = 0, pady=30)            


      
    def highlight_buttons(self):
        #since this function is scheduled and called, we are checking a flag whether highlight is required or not
        if self.highlight_flag == 1:
            
            
            for lbl in self.label_widgets:
                lbl.config(bg=BCOLOR)  # Reset the background color of all buttons
            
            lbl_to_highlight = self.label_widgets[self.highlight_index]
            lbl_to_highlight.config(bg=HCOLOR)  # Highlight the current button

            if self.flag == 0:
                self.flag = 1
            else:
                self.counter = self.counter + 1
                if self.counter>=len(self.scan_list):
                    self.counter = 0
                speak_text = self.scan_list[self.highlight_index-1]
                self.engine.say(speak_text)
                self.engine.runAndWait()
            self.highlight_index = (self.highlight_index + 1) % len(self.label_widgets)  # Move to the next button
            self.master.after(1000, self.highlight_buttons)  # Schedule the next highlight
    
    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def on_mouse_click(self,event):
        
        if self.counter == 0:
            self.actual_index =  len(self.button_widgets)-1
        else:
            self.actual_index = self.counter - 1
        
        print("indexes clicked in scan select exercise ..",self.highlight_index, self.actual_index,self.counter)
        self.highlight_flag = 0
    
        self.scan_selected_questions()

    def scan_selected_questions(self):
        my_result=[]
        self.clear_frame(self.display_frame)
        self.clear_frame(self.header_frame)
        
        if self.category == "Alphabet Scramble":
            self.questions_list = db.get_questions_for_game1_exercise(self.exercise_list[self.actual_index][0],self.teacher_id)
            print("1 here")
            print(self.questions_list)
            if len(self.questions_list)!=0:
                ssqg1.ScanSelectedQuestionsDisplayGame1(self.master,self.header_frame,self.display_frame,self.student_id,self.teacher_id,self.scan_list[self.actual_index],self.category,self.questions_list,0,my_result)
        elif self.category == "Sentence Builder":
            self.questions_list = db.get_questions_for_game2_exercise(self.exercise_list[self.actual_index][0],self.teacher_id)
            print("2 here")
            print(self.questions_list)
            if len(self.questions_list)!=0:
                ssqg2.ScanSelectedQuestionsDisplayGame2(self.master,self.header_frame,self.display_frame,self.student_id,self.teacher_id,self.scan_list[self.actual_index],self.category, self.questions_list,0,my_result)
        elif self.category == "Objective Type":
            self.questions_list = db.get_questions_for_game3_exercise(self.exercise_list[self.actual_index][0],self.teacher_id)
            print("3 here")
            print(self.questions_list)
            if len(self.questions_list)!=0:
                ssqg3.ScanSelectedQuestionsDisplayGame3(self.master,self.header_frame,self.display_frame,self.student_id,self.teacher_id,self.scan_list[self.actual_index],self.category,self.questions_list,0,my_result)
        else:
            self.questions_list = db.get_questions_for_game4_exercise(self.exercise_list[self.actual_index][0],self.teacher_id)
            print("4 here")
            print(self.questions_list)
            if len(self.questions_list)!=0:
                self.header_frame.destroy()
                self.display_frame.destroy()
                self.master.destroy()
                root = tk.Tk()
                header_frame=tk.Frame(root,background="cyan4")
                header_frame.grid()
                display_frame=tk.Frame(root,background="cyan4")
                display_frame.grid()
                ssqg4.ScanSelectedQuestionsDisplayGame4(root,header_frame,display_frame,self.student_id,self.teacher_id,self.scan_list[self.actual_index],self.category,self.questions_list,0,my_result)
        
        if len(self.questions_list) == 0:
                messagebox.showerror('student section', "There is no questions assigned to this exercise. Contact your teacher!")
                self.header_frame.destroy()
                self.display_frame.destroy()
                self.master.destroy()
                root = tk.Tk()
                ssc.ScanSelectCategory(root,self.student_id,self.teacher_id)
     