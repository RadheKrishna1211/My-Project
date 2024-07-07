import tkinter as tk
from tkinter import ttk
import database_code as db
from tkinter import messagebox
import password_encryption as pe
from tkinter.font import Font
import scan_select_category as ssc
import student_login_screen as sl


class StudentLoginScreen:
    def __init__(self,master):
        self.master = master
        db.create_tables()
        self.master.state('zoomed')#automatically expands window to full size
        self.master.title("Inclusive Scan and Play Software")
        self.master.configure(bg='cyan4')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.main_screen_header_frame = tk.Frame(self.master,background="cyan4")
        self.main_screen_header_frame.grid()

        self.login_screen_frame = tk.Frame(self.master,background="cyan4")
        self.login_screen_frame.grid()

        self.create_main_screen_header("Login page for the Students! ")
        self.create_student_login_screen()

    def create_main_screen_header(self,header_text):
        main_screen_header_label = tk.Label(self.main_screen_header_frame, text=header_text, bg='cyan4', fg='white', font=('Arial',30))
        main_screen_header_label.grid( row=0,column=1)
           
    def create_student_login_screen(self):
        self.lbl_user_name=tk.Label(self.login_screen_frame,text='User Name :',font=('Arial',20),bg='Cyan4',fg='White')
        self.lbl_user_name.grid(row=1,column=0,sticky = 'W', pady = 20)
        
        self.lbl_password=tk.Label(self.login_screen_frame,text='Password :',font=('Arial',20),bg='Cyan4',fg='White')
        self.lbl_password.grid(row=2,column=0,sticky = 'W', pady = 20)

        self.lbl_teacher_id=tk.Label(self.login_screen_frame,text='Teacher User Name :',font=('Arial',20),bg='Cyan4',fg='White')
        self.lbl_teacher_id.grid(row=3,column=0,sticky = 'W', pady = 20)

        self.txtbox_user_name=tk.Entry(self.login_screen_frame,font=('Arial',20))
        self.txtbox_user_name.grid(row=1,column=1,sticky = 'W', pady = 20)

        self.txtbox_password=tk.Entry(self.login_screen_frame, font=('Arial',20),show="*")
        self.txtbox_password.grid(row=2,column=1,sticky = 'W', pady = 20)
        teacher_list=db.get_teacher_user_names() 
        
        if teacher_list== False:
            messagebox.showerror('login','No Teachers are Registered!!')
        else:
            # Adding combobox drop down list 
            self.combo_teacher_name = ttk.Combobox(self.login_screen_frame, width = 35, font=('Arial',20), values = teacher_list)
                   
            self.combo_teacher_name.grid(row = 3,column = 1)
        
        self.btn_login=tk.Button(self.login_screen_frame,text='Login',bg='cyan3',font=('Arial',15), command=self.login)
        self.btn_login.grid(row=4,column=1, pady = (20,200))

        self.btn_cancel=tk.Button(self.login_screen_frame,text='Cancel',bg='cyan3',font=('Arial',15), command=self.cancel_command)
        self.btn_cancel.grid(row=4,column=0, pady = (20,200))

    def cancel_command(self):

        messagebox.askokcancel("Login Exit","Do you want to cancel?")
        self.clear_frame(self.header_frame)
        self.clear_frame(self.display_frame)
        sl.StudentLoginScreen(self.master)
        
    def login(self):
        user_name=self.txtbox_user_name.get()
        password=self.txtbox_password.get()
        teacher_user_name=self.combo_teacher_name.get()
        if user_name=='' or password=='' or teacher_user_name=='':
            messagebox.showerror('login','Blanks are not allowed')
        else:
            teacher_id =db.get_teacher_id(teacher_user_name)
            if teacher_id==False:
                messagebox.showerror('login','Teacher user name is incorrect')
            else:
                result = db.check_student_password_match(user_name,pe.encrypt_password(password),teacher_id)
                #print(result)

                if  result == False:
                    messagebox.showerror('login','User Name or Password or teacher selected is incorrect')
                else:
                    messagebox.showinfo('login','login successful')
                    student_id=db.get_student_id(user_name,teacher_id)   
                    self.show_student_screen(student_id,teacher_id)
                    #self.StudentMainScreen()
            
           
    
    def show_student_screen(self,student_id, teacher_id):
           self.main_screen_header_frame.destroy()
           self.login_screen_frame.destroy()
           ssc.ScanSelectCategory(self.master,student_id, teacher_id)

    def run(self):
        self.mainloop()

def main():
    root = tk.Tk()
    StudentLoginScreen(root)
    font = Font(family = "Arial", size = 20)
    root.option_add("*TCombobox*Listbox*Font", font)
    root.mainloop()

if __name__ == "__main__":
    main()