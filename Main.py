import tkinter as tk
from ToDoListApp import ToDoListApp

def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()