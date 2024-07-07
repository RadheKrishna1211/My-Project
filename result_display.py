import tkinter as tk
from tkinter import messagebox
import pyttsx3
import scan_select_exercise as se
import database_code as db
import scan_select_category as ssc
from random import shuffle

HCOLOR = "yellow"
BCOLOR = "cyan4"
FCOLOR = "white"
TITLEFG = '#2D1BA6'
TITLEBG = '#ffffcc'

class ScanSelectedQuestionsDisplayGame1:
    def __init__(self, master, header_frame, display_frame, student_id, teacher_id, selected_exercise_name, selected_exercise_id, category,exercise_questions, current_index,result ):
        
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.header_frame = header_frame
        self.display_frame=display_frame
        self.master = master
        self.exercise_name = selected_exercise_name
        self.exercise_id = selected_exercise_id
        self.exercise_questions = exercise_questions
        self.current_index = current_index
        self.game1_final_result = result
        self.game1_result = ""
       
        self.category = category
        self.scan_list = self.get_scan_list_from_word(self.exercise_questions[self.current_index])

        self.title = "Form a word from these letters!"
        
        self.master.title("Inclusive Scan and Play Software")
        self.master.state('zoomed')#automatically expands window to full size
        
        self.master.configure(bg='cyan4')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.header_frame,  font=("Arial",30,"bold"),width=50, background=TITLEBG,fg=TITLEFG)
        self.title_label.grid(row=0, column = 0)
        
        self.title_label.configure(text=self.title)
        
        self.game1_result_header_label = tk.Label(self.display_frame,  font=("Arial",30,"bold"),width=30, bg=TITLEBG,fg=TITLEFG)
    
        self.variable_initializations()
        self.voice_initializations()
        self.create_buttons()
        self.master.after(100, self.highlight_buttons) 

        self.master.bind('<Button-1>', self.on_mouse_click)

    def get_scan_list_from_word(self, exercise_question):
        scan_list=[]
        word = exercise_question[1]
        word =  list(word)
        shuffle(word)
        for letter in word:
            scan_list.append(letter)
        scan_list.append("Cancel")
        scan_list.append("Submit")
        return scan_list
            
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
        for i in range(0,len(self.scan_list)-2): 
            rowval = i//2
            colval = i%2
            self.surround_label = tk.Label(self.display_frame, height=50,width=300, background=BCOLOR)
            button = tk.Button(self.surround_label,height=2, font=("Arial",20,"bold"), width=30,background=BCOLOR,fg=FCOLOR)
            self.surround_label.grid(row=rowval,column=colval)     
            button.grid(row=rowval, column=colval, pady=10,padx=20)
            button.configure(text=self.scan_list[i])
            self.button_widgets.append(button)             
            self.label_widgets.append(self.surround_label)
        
        rowval = rowval + 1
        colval = 0
        self.surround_label = tk.Label(self.display_frame, height=50,width=300, background=BCOLOR)
        button = tk.Button(self.surround_label,height=2, font=("Arial",20,"bold"), width=30,background=BCOLOR,fg=FCOLOR)
        self.surround_label.grid(row=rowval,column=colval)     
        button.grid(row=rowval, column=colval, pady=10,padx=20)
        button.configure(text=self.scan_list[-2])
        self.button_widgets.append(button)             
        self.label_widgets.append(self.surround_label)
        colval = 1
        self.surround_label = tk.Label(self.display_frame, height=50,width=300, background=BCOLOR)
        button = tk.Button(self.surround_label,height=2, font=("Arial",20,"bold"), width=30,background=BCOLOR,fg=FCOLOR)
        self.surround_label.grid(row=rowval,column=colval)     
        button.grid(row=rowval, column=colval, pady=10,padx=20)
        button.configure(text=self.scan_list[-1])
        self.button_widgets.append(button)             
        self.label_widgets.append(self.surround_label)
            
        
        rowval= rowval + 1
        self.game1_result_header_label.grid(row=rowval, column = 0, columnspan=2, pady=50)            


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
        print("on mouse click...SELECT EXERCISE WINDOW")
        
        if self.counter == 0:
            self.actual_index =  len(self.button_widgets)-1
        else:
            self.actual_index = self.counter - 1
        
        print("indexes clicked..",self.highlight_index, self.actual_index,self.counter)
        
        #this is just a protection that the actual index should not be more than the length of the contents
        if self.actual_index >= len(self.button_widgets):
            self.actual_index = len(self.button_widgets)-1
        
        if self.actual_index == len(self.scan_list) -2:
            print("cancel")
            if len(self.game1_result)!=0:
                self.game1_result = self.game1_result.rstrip(self.game1_result[-1])
                self.game1_result_header_label.configure(text=self.game1_result)
        elif self.actual_index == len(self.scan_list) - 1:
            print("submit")
            self.game1_final_result.append(self.game1_result)
            print("my results.....",self.game1_result,self.game1_final_result)
            self.highlight_flag = 0
            self.clear_frame(self.display_frame)
            self.clear_frame(self.header_frame)
            self.current_index = self.current_index + 1
            if self.current_index >= len(self.exercise_questions):
                print("OVER")
            else:
                ScanSelectedQuestionsDisplayGame1(self.master,self.header_frame,self.display_frame,1,1,"Scramble",1, "Alphabet Scramble", self.exercise_questions, self.current_index, self.game1_final_result)

        else:
            val = self.scan_list[self.actual_index]
            print("my val", val)
            self.game1_result = self.game1_result + val
            print("result.....",self.scan_list, self.game1_result,self.actual_index,self.scan_list[self.actual_index])
           
            self.game1_result_header_label.configure(text=self.game1_result)
        
        
    
       ###############################################3

def main():
    root = tk.Tk()
    header_frame=tk.Frame(root,background="cyan4")
    header_frame.grid()
    display_frame=tk.Frame(root,background="cyan4")
    display_frame.grid()

    ex_questions = [[1,"gave"],[2,"hope"]]
    my_result = [] 
    ScanSelectedQuestionsDisplayGame1(root,header_frame,display_frame,1,1,"Scramble",1, "Alphabet Scramble", ex_questions, 0, my_result)
    root.mainloop()

if __name__ == "__main__":
    main()
        