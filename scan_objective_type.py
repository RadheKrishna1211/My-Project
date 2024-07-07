import tkinter as tk
import pyttsx3
import sounddevice as sd
import soundfile as sf
import time
from PIL import Image, ImageTk
HCOLOR = "yellow"
BCOLOR = "cyan4"

class ScanTest:
    def __init__(self, master,header_frame,display_frame,objective_questions_list,objective_answers_list):
        
        #self.teacher_id = teacher_id
        self.header_frame = header_frame
        self.display_frame=display_frame
        self.master = master
        self.objective_questions_list = objective_questions_list
        self.objective_answers_list = objective_answers_list

        self.master.title("Inclusive Scan and Play Software")
        self.master.state('zoomed')#automatically expands window to full size
        
        self.master.configure(bg='cyan4')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.question_header_label = tk.Label(self.header_frame,  font=("Arial",30,"bold"),width=50, background='#ffffcc',fg='#2D1BA6')
        self.question_header_label.grid(row=0, column = 0)
        print("Quest:::",self.objective_questions_list[0])
        self.question_header_label.configure(text=self.objective_questions_list[0])
       
        self.variable_initializations()

        
        self.voice_initializations()
        self.create_buttons()
        self.highlight_buttons()

        self.master.bind('<Button-1>', self.on_mouse_click)

    def variable_initializations(self):
        self.highlight_flag = 1
        self.flag = 0
        self.label_widgets = []
        self.button_widgets = []
        self.counter = 0
        self.highlight_index = 0
        self.result_list = []  
        self.question_count = 0
        self.answer_speak = self.objective_answers_list[0]

        

    def voice_initializations(self):
        self.engine = pyttsx3.init()
        self.engine. setProperty("rate",150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)#female voice
 

    def create_buttons(self):
        for i in range(0,len(self.objective_answers_list[0])): 
            
            self.surround_label = tk.Label(self.display_frame, height=300,width=300, background=BCOLOR)
            rowval = i//2
            colval = i%2
            self.surround_label.grid(row=rowval,column=colval)     
            button = tk.Button(self.surround_label,height=5, font=("Arial",20,"bold"), width=30,background=BCOLOR,fg='#2D1BA6')
            button.grid(row=rowval, column=colval, pady=10,padx=20)
            self.button_widgets.append(button)

            button.configure(text=self.objective_answers_list[0][i])
            
            self.label_widgets.append(self.surround_label)

      
    def highlight_buttons(self):
        #since this function is scheduled and called, we are checking a flag whether highlight is required or not
        if self.highlight_flag == 1:
            self.counter = self.counter + 1
            if self.counter>=len(self.objective_answers_list[0]):
                self.counter = 0
            
            for lbl in self.label_widgets:
                lbl.config(bg=BCOLOR)  # Reset the background color of all buttons
            
            lbl_to_highlight = self.label_widgets[self.highlight_index]
            lbl_to_highlight.config(bg=HCOLOR)  # Highlight the current button

            if self.flag == 0:
                self.flag = 1
            else:
                speak_text = self.answer_speak[self.highlight_index-1]
                self.engine.say(speak_text)
                self.engine.runAndWait()
            self.highlight_index = (self.highlight_index + 1) % len(self.label_widgets)  # Move to the next button
            self.master.after(1000, self.highlight_buttons)  # Schedule the next highlight
    
    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def on_mouse_click(self,event):
        print("hello...................................................")
        print(self.highlight_index)
        self.actual_index = -1
        if self.highlight_index == 0:
            self.actual_index =  3
        elif self.highlight_index == 1:
            self.actual_index =  4
        else:
            self.actual_index = self.highlight_index - 1
        print(self.actual_index)
        self.result_list = self.result_list.append(self.actual_index)
        print("question count....")
        self.question_count = self.question_count + 1
        print(self.question_count,self.objective_questions_list)
        if self.question_count < len(self.objective_questions_list):
            
            print("inside if....")
            i=0
            self.question_header_label.configure(text=self.objective_questions_list[self.question_count])
            
            self.answer_speak = self.objective_answers_list[self.question_count]
            for button in self.button_widgets:
                print("inside configurng button widgets....")
                print(self.objective_answers_list[self.question_count][i])
                button.configure(text=self.objective_answers_list[self.question_count][i])
                i = i + 1
            self.highlight_index=0
            self.flag=0
            self.counter=0

                ###############################################3
        else:
            self.highlight_flag = 0
            self.clear_frame(self.display_frame)
            self.clear_frame(self.header_frame)


       ###############################################3
        
        #self.master.destroy()


def main():
    root = tk.Tk()
    header_frame=tk.Frame(root,background="cyan4")
    header_frame.grid()
    display_frame=tk.Frame(root,background="cyan4")
    display_frame.grid()

    objective_questions_list = ['Question 1','Question 2','Question 3']

    objective_answers_list = [ ['OPTION 11', 'OPTION 12', 'OPTION 13','OPTION 14'],
                              ['OPTION 21', 'OPTION 22', 'OPTION 23','OPTION 24'],
                               ['OPTION 31', 'OPTION 32', 'OPTION 33','OPTION 34'] 
                               ]
    
    ScanTest(root,header_frame,display_frame,objective_questions_list,objective_answers_list)
    root.mainloop()

if __name__ == "__main__":
    main()
        