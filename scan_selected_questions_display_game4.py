import tkinter as tk
import pyttsx3
from PIL import Image, ImageTk
import scan_student_result_page_game4 as ssrp


HCOLOR = "yellow"
BCOLOR = "cyan4"
FCOLOR = "white"
TITLEFG = '#2D1BA6'
TITLEBG = '#ffffcc'

class ScanSelectedQuestionsDisplayGame4:
    def __init__(self, master,header_frame,display_frame,student_id, teacher_id, selected_exercise_name, category,exercise_questions, current_index,result):
        
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.header_frame = header_frame
        self.display_frame=display_frame
        self.master = master
        self.exercise_name = selected_exercise_name
        
        self.exercise_questions = exercise_questions
        self.current_index = current_index
        self.game4_final_result = result
        self.game4_result = ""
        self.category = category
        self.scan_list = self.get_scan_list(self.exercise_questions[self.current_index])
        self.game4_result_number=0
        #print(self.scan_list)
        self.text_to_speak = ['OPTION 1', 'OPTION 2', 'OPTION 3','OPTION 4', 'Cancel', 'Submit']
        self.title = "Select the Odd Image Out"
        

        self.master.title("Inclusive Scan and Play Software")
        self.master.state('zoomed')#automatically expands window to full size
        
        self.master.configure(bg='cyan4')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.game4_result_header_label = tk.Label(self.display_frame,  font=("Arial",30,"bold"),width=30, bg=TITLEBG,fg=TITLEFG)
        self.variable_initializations()

        title_label = tk.Label(self.header_frame, font=("Arial",30,"bold"),background='#ffffcc',fg='#2D1BA6')
        title_label.grid(row=0, column = 1)
        title_label.configure(text=self.title)      
        self.voice_initializations()

        self.create_buttons()
        self.highlight_buttons()

        self.master.bind('<Button-1>', self.on_mouse_click)

    def variable_initializations(self):
        self.highlight_flag = 1
        self.first_screen_flag = 0
        self.button_widgets = []
        self.label_widgets = []
        self.counter = 0
        self.highlight_index = 0
        

    def voice_initializations(self):
        self.engine = pyttsx3.init()
        self.engine. setProperty("rate",150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)#female voice
 

    def create_buttons(self):
        self.button_widgets = []
        self.label_widgets = []
        self.image_object_list=[]
        for i in range(0,len(self.text_to_speak)-2):
            self.image1 = Image.open(self.scan_list[i])
            self.image_object_list.append(ImageTk.PhotoImage(self.image1))

        for i in range(0,len(self.scan_list)-2): 
            
            self.image_label = tk.Label(self.display_frame, height=300,width=300, background=BCOLOR)
            rowval = i//2
            colval = i%2
            self.image_label.grid(row=rowval,column=colval)     
            button = tk.Button(self.image_label,height=150, font=("Arial",20,"bold"),width=300,background=BCOLOR,fg='#2D1BA6')
            button.grid(row=rowval, column=colval, pady=10,padx=20)

            button.configure(image=self.image_object_list[i])
            self.button_widgets.append(button)
            self.label_widgets.append(self.image_label)
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
        self.game4_result_header_label.grid(row=rowval, column = 0, columnspan=2, pady=20)            


    def highlight_buttons(self):
        #since this function is scheduled and called, we are checking a flag whether highlight is required or not
        if self.highlight_flag == 1:
            self.counter = self.counter + 1
            #print("in highlight, first screen counter incremented", self.counter)
            #print(self.counter)
            if self.counter>=len(self.text_to_speak):
                self.counter = 0
                #print("in highlight, first screen counter reset", self.counter)
            #print(self.highlight_index)
            for button in self.label_widgets:
                button.config(bg=BCOLOR)  # Reset the background color of all buttons
            
            button_to_highlight = self.label_widgets[self.highlight_index]
            button_to_highlight.config(bg="yellow")  # Highlight the current button

            if self.first_screen_flag == 0:
                self.first_screen_flag = 1
            else:
                speak_text = self.text_to_speak[self.highlight_index-1]
                self.engine.say(speak_text)
                self.engine.runAndWait()
            self.highlight_index = (self.highlight_index + 1) % len(self.label_widgets)  # Move to the next button
            self.master.after(1000, self.highlight_buttons)  # Schedule the next highlight

    def get_scan_list(self, exercise_question):
        scan_list=[]
        for i in range(2,6):
            scan_list.append(exercise_question[i])
        #print("option list in scanlist ", scan_list)
        scan_list.append("Cancel")
        scan_list.append("Submit")
        return scan_list
    
    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()
    
    def on_mouse_click(self,event):

        #################################################################################3
        print("on mouse click...counter....",self.counter)
        print("scan list length", len(self.scan_list))
        self.actual_index = self.counter-2
        if self.actual_index <0:
            self.actual_index = self.actual_index + len(self.scan_list)
        
        print("indexes clicked..actual index and counter", self.actual_index,self.counter)
        
        if self.actual_index == len(self.scan_list) -2:
            print("cancel")
            self.game4_result_number=0
            self.game4_result=""
            self.game4_result_header_label.configure(text=self.game4_result)
        elif self.actual_index == len(self.scan_list)-1:
            print("submit")
            self.game4_final_result.append(self.game4_result_number)
            print("my results.....",self.game4_result,self.game4_final_result)
            self.highlight_flag = 0
            self.clear_frame(self.display_frame)
            self.clear_frame(self.header_frame)
            self.current_index = self.current_index + 1
            if self.current_index >= len(self.exercise_questions):
                print("OVER")
                ssrp.ScanStudentResultPageGame4(self.master, self.header_frame, self.display_frame,self.student_id, self.teacher_id, self.exercise_name, self.category, self.exercise_questions, self.game4_final_result)
            else:
                ScanSelectedQuestionsDisplayGame4(self.master,self.header_frame,self.display_frame,self.student_id,self.teacher_id,self.exercise_name,self.category, self.exercise_questions, self.current_index, self.game4_final_result)

        else:
            print("NEED ACTUAL INDEX", self.actual_index)
            val = self.text_to_speak[self.actual_index]
            self.game4_result = val
            self.game4_result_number = self.actual_index + 1
            #print("result.....",self.scan_list, self.game4_result,self.actual_index,self.scan_list[self.actual_index])
            self.game4_result_header_label.configure(text=self.game4_result)
        
