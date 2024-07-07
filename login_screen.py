import tkinter as tk
import database_code as db
from tkinter import messagebox
import teacher_menu.teacher_menu as thm
import teacher_menu.teacher_register_screen as trgs
import password_encryption as pe
import student_login_screen as sl

class LoginScreen:
    def __init__(self,master, header_frame, display_frame):
        
        self.master = master
        db.create_tables()
        self.master.state('zoomed')#automatically expands window to full size
        self.master.title("Inclusive Scan and Play Software")
        self.master.configure(bg='cyan4')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.header_frame = header_frame
        self.display_frame = display_frame

        self.create_main_screen_header("Login page for the teacher! ")
        self.create_login_screen()
        
    def create_main_screen_header(self,header_text):
        main_screen_header_label = tk.Label(self.header_frame, text=header_text, bg='cyan4', fg='white', font=('Arial',30))
        main_screen_header_label.grid( row=0,column=1)
        
    def create_login_screen(self):
        self.lbl_user_name=tk.Label(self.display_frame,text='User Name :',font=('Arial',20),bg='Cyan4',fg='White')
        self.lbl_user_name.grid(row=1,column=0,sticky = 'W', pady = 20)
        
        self.lbl_password=tk.Label(self.display_frame,text='Password :',font=('Arial',20),bg='Cyan4',fg='White')
        self.lbl_password.grid(row=2,column=0,sticky = 'W', pady = 20)

        self.txtbox_user_name=tk.Entry(self.display_frame,font=('Arial',20))
        self.txtbox_user_name.grid(row=1,column=1,sticky = 'W', pady = 20)

        self.txtbox_password=tk.Entry(self.display_frame, font=('Arial',20),show="*")
        self.txtbox_password.grid(row=2,column=1,sticky = 'W', pady = 20)
        self.btn_login=tk.Button(self.display_frame,text='Login',bg='cyan3',font=('Arial',15), command=self.login)
        self.btn_login.grid(row=3,column=1, pady = (20,20))    
        
        self.btn_register=tk.Button(self.display_frame,text='New User? Register',bg='cyan3',font=('Arial',15), command=self.new_register)
        self.btn_register.grid(row=3,column=0, sticky = 'E', pady = (20,20))

        self.btn_login_std=tk.Button(self.display_frame,text='If you are student,click here! ',bg='yellow',font=('Arial',15), command=self.student_login)
        self.btn_login_std.grid(row=4,column=0,columnspan=2, pady = (20,200)) 
        
    def show_teacher_menu_screen(self,teacher_id):
           self.header_frame.destroy()
           self.display_frame.destroy()
           thm.TeacherMenuBar(self.master,teacher_id)

    def show_registration_screen(self):
           self.header_frame.destroy()
           self.display_frame.destroy()
           trgs.RegisterScreen(self.master)

    def login(self):
        user_name=self.txtbox_user_name.get()
        teacher_id = db.get_teacher_id(user_name)
        password=self.txtbox_password.get()
        result = db.check_teacher_user_password_match(user_name,pe.encrypt_password(password))
        print(result)
        if user_name=='' or password=='':
            messagebox.showerror('login','Blanks are not allowed')
        elif  result == False:
            messagebox.showerror('login','User Name or Password is incorrect')
        else:
            if teacher_id == False:
                messagebox.showerror('login','User Name or Password is incorrect')  
            else:
                messagebox.showinfo('login','Welcome Teacher!!! login successful')        
                self.show_teacher_menu_screen(teacher_id)

    def student_login(self):
        self.header_frame.destroy()
        self.display_frame.destroy()
        sl.StudentLoginScreen(self.master)

  
    def new_register(self):
        self.header_frame.destroy()
        self.display_frame.destroy()
        self.show_registration_screen()

