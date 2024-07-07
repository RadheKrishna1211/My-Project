import tkinter as tk
import pyttsx3
import scan_select_exercise as se
import student_login_screen as sls
from tkinter import messagebox

HCOLOR = "yellow"
BCOLOR = "cyan4"
FCOLOR = "white"

class ScanSelectCategory:
    def __init__(self, master,student_id, teacher_id):
    
        self.teacher_id = teacher_id
        self.student_id = student_id
       
        self.master = master
        self.title = "Select the Category!!"
        self.scan_list = ['Alphabet Scramble', 'Sentence Builder', 'Objective Type','Odd One Out Image','Cancel','Exit']
    
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
            button = tk.Button(self.surround_label,height=3, font=("Arial",20,"bold"), width=30,background=BCOLOR,fg=FCOLOR)
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
        #print("on mouse click...")
        #print(self.counter)
        #print("###########################################")
        self.highlight_flag = 0
        if self.counter == 0:
            self.actual_index =  len(self.button_widgets)-1
        else:
            self.actual_index = self.counter - 1
        
        if self.actual_index==4:
            self.clear_frame(self.display_frame)
            self.clear_frame(self.header_frame)
            self.display_frame.destroy()
            self.header_frame.destroy()
            sls.StudentLoginScreen(self.master)
        elif self.actual_index==5:
            messagebox.showerror('Scan Category','Thank you for using inclusivePlay:Scan & Learn')
            self.clear_frame(self.display_frame)
            self.clear_frame(self.header_frame)
            self.display_frame.destroy()
            self.header_frame.destroy()
            self.master.destroy()
        else:               
            self.clear_frame(self.display_frame)
            self.clear_frame(self.header_frame)
        
            root = tk.Tk()
            header_frame1=tk.Frame(root,background="cyan4")
            header_frame1.grid()
            display_frame1=tk.Frame(root,background="cyan4")
            display_frame1.grid()
            
            self.display_frame.destroy()
            self.header_frame.destroy()
            self.master.destroy()
            #se.ScanSelectExercise(root,header_frame1, display_frame1,0, 1,1,"Alphabet Scramble")
            se.ScanSelectExercise(root,header_frame1,display_frame1,self.actual_index, self.student_id, self.teacher_id, self.scan_list[self.actual_index])
        