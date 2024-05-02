import tkinter as tk
import json
import os

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TODO List App")
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.x = (self.screen_width/2) - (1280/2)
        self.y = (self.screen_height/2) - (720/2)

        self.root.geometry(f"1280x720+{int(self.x)}+{int(self.y-50)}")

        # Load the background image
        #self.bg_image = tk.PhotoImage(file="bg1.png")
        #self.bg_label = tk.Label(self.root, image=self.bg_image)
        #self.bg_label.place(relwidth=1, relheight=1)

        # Create frames for todo and done lists
        self.todo_frame = tk.Frame(self.root,background="grey")
        self.done_frame = tk.Frame(self.root, background="grey")
        self.button_frame = tk.Frame(self.root)

        # Create labels and lists for todo and done lists
        self.todo_label = tk.Label(self.todo_frame, text="TODO:", font=("Comic Sans MS", 20, "bold"), background="grey")
        self.todo_list = tk.Listbox(self.todo_frame, width=100, height=6, font=("Comic Sans MS", 15, "bold"), background="lightblue")
        self.done_label = tk.Label(self.done_frame, text="DONE",font=("Comic Sans MS", 20, "bold"), background="grey")
        self.done_list = tk.Listbox(self.done_frame, width=100, height=6, font=("Comic Sans MS", 15, "bold"), background="lightgreen")

        # Create entry field and buttons for adding and completing tasks
        self.entry_field = tk.Entry(self.root, width=180,font=("Comic Sans MS", 15, "bold"),background="yellow")
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task, border=5, font=("Comic Sans MS", 15, "bold"))
        self.complete_button = tk.Button(self.root, text="I completed the task", command=self.complete_task, border=5, font=("Comic Sans MS", 15, "bold"))
        self.delete_button = tk.Button(self.root, text="DELETE TASK", command=self.delete_task, border=5, font=("Comic Sans MS", 15, "bold"))
        self.reset_button = tk.Button(self.root, text="RESET", command=self.reset_task, border=5, font=("Comic Sans MS", 15, "bold"))
        self.entry_field.bind("<Return>", lambda event: self.add_task())
        self.root.bind("<Delete>", lambda event: self.delete_task()) 
        self.root.bind("<r>", lambda event:self.reset_task())
        
        # Load data from file
        self.data_file = 'todo_list.json'
        self.load_data()

        # Pack everything
        self.todo_frame.pack()
        self.todo_label.pack()
        self.todo_list.pack()
        self.complete_button.pack()
        self.delete_button.pack()
        self.reset_button.pack()
        
        self.done_frame.pack()
        self.done_label.pack(pady=10)
        self.done_list.pack()
        self.entry_field.pack()
        self.add_button.pack()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                for task in data['todo']:
                    self.todo_list.insert(tk.END, task)
                for task in data['done']:
                    self.done_list.insert(tk.END, task)

    def save_data(self):
        data = {'todo': self.todo_list.get(0, tk.END), 'done': self.done_list.get(0, tk.END)}
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def add_task(self):
        task = self.entry_field.get()
        if task:
            self.todo_list.insert(tk.END, task)
            self.entry_field.delete(0, tk.END)
            self.save_data()

    def complete_task(self):
        selected_task = self.todo_list.curselection()
        if selected_task:
            task = self.todo_list.get(selected_task)
            self.todo_list.delete(selected_task)
            self.done_list.insert(tk.END, task)
            self.save_data()

    def delete_task(self):
        task1 = self.done_list.curselection()
        task2 = self.todo_list.curselection()
        if task1:
            self.done_list.delete(task1[0])
            self.save_data()
        elif task2:
            self.todo_list.delete(task2[0])
            self.save_data()

    def reset_task(self):
        task1 = self.done_list.curselection()
        task2 = self.todo_list.curselection()

        if task1 or task2:
            self.todo_list.delete(0, tk.END)
            self.done_list.delete(0, tk.END)
            self.save_data()

root = tk.Tk()
app = TodoListApp(root)
root.mainloop()