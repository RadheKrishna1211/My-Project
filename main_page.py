import tkinter as tk
import login_screen as ls

def main():
    root = tk.Tk()
    header_frame = tk.Frame(root,background="cyan4")
    header_frame.grid()

    display_frame = tk.Frame(root,background="cyan4")
    display_frame.grid()
    ls.LoginScreen(root, header_frame,display_frame)
    root.mainloop()

if __name__ == "__main__":
    main()