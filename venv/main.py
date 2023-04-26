import tkinter as tk
import time
from tkinter import ttk
import dayPlanner as DayPlanner
import stockConsistency as SC
import pandas as pd
import datetime
import os

# ADD A DATAFRAME
date = datetime.datetime.now()
filename = date.strftime('Day-Plan-%m-%d-%Y.csv')
df = pd.read_csv(f"C:\\Users\\yagof\\IdeaProjects\\scheduleez\\venv\\dayPlans\\{filename}")

class ScheduleScreen(tk.Frame):
    def __init__(self, master, **kwargs):

        super().__init__(master, bg="black", **kwargs)

        if not os.path.isfile(f"C:\\Users\\yagof\\IdeaProjects\\scheduleez\\venv\\dayPlans\\{filename}"):
            tk.messagebox.showerror("File not found", f"No file found for {date_str}.")
            return


        tk.Label(self, text="Schedule", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=10)
        button = tk.Button(self, text="Edit", font=("Arial", 12, "bold"), fg="white", bg="black", command=self.show_list)
        button.pack(fill="both", expand=False)
        self.list_shown = False


        # Create a container to hold the day columns
        self.day_container = tk.Frame(self, bg="white")
        self.day_container.pack(fill="both", expand=True, padx=10, pady=10)


        # Create a canvas for each day column
        self.day_canvases = []
        self.day_frames = []
        self.day_scrollbars = []


        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            day_canvas = tk.Canvas(self.day_container, bg="white", highlightthickness=0)
            day_frame = tk.Frame(day_canvas, bg="white")
            day_scrollbar = tk.Scrollbar(self.day_container, orient="vertical", command=day_canvas.yview)
            day_canvas.configure(yscrollcommand=day_scrollbar.set)
            day_canvas.pack(side="left", fill="both", expand=True)
            day_scrollbar.pack(side="left", fill="y", pady=(0, 10), padx=(0, 5))
            self.day_canvases.append(day_canvas)
            self.day_frames.append(day_frame)
            self.day_scrollbars.append(day_scrollbar)

                # Create labels for the hours of the day
            if day == "Monday":
                for hour in range(5, 24):
                    hour_label = tk.Label(day_frame, text=f"{hour}:00", bg="white")
                    hour_label.pack(fill="x")
                    for i in range(288):
                        if i > 60:
                            time = datetime.time(hour=i // 12, minute=(i % 12) * 5)
                            row = df.loc[df['Time'] == time.strftime('%H:%M')]
                            task_text = row.iloc[0]["Text"]
                            task_label = tk.Label(day_frame, text=task_text, bg="white")
                            task_label.pack()

            day_canvas.create_window((0, 0), window=day_frame, anchor="nw")
            day_frame.bind("<Configure>", lambda event, canvas=day_canvas: self.on_frame_configure(canvas))

        # Create a binding to resize the columns when the window is resized
        self.day_container.bind("<Configure>", self.on_container_configure)

    def on_container_configure(self, event):
        # Resize each day column to have the same width
        width = self.day_container.winfo_width() // 7
        for canvas in self.day_canvases:
            canvas.config(width=width)

    def on_frame_configure(self, canvas):
        # Resize the canvas scroll region when the frame size changes
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_list(self):
        if not self.list_shown:
            self.list_shown = True
            toplevel = tk.Toplevel(self)
            app = DayPlanner.DayPlanner(toplevel)
            toplevel.protocol("WM_DELETE_WINDOW", lambda: self.on_close(toplevel))

    def on_close(self, toplevel):
        self.list_shown = False
        toplevel.destroy()


class ProgressScreen(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        tk.Label(self, text="Progress", font=("Arial", 16, "bold"), fg="black").pack(pady=10)
        button = tk.Button(self, text="Open", font=("Arial", 12, "bold"), fg="white", bg="black", command=self.showWLGraph)
        button.pack(fill="both", expand=True)
        self.WLG_shown = False

    def showWLGraph(self):
        if not self.WLG_shown:
            self.WLG_shown = True
            toplevel = tk.Toplevel(self)
            app = SC.stockConsistency(toplevel)
            toplevel.protocol("WM_DELETE_WINDOW", lambda: self.on_close_WLG(toplevel))

    def on_close_WLG(self, toplevel):
        self.WLG_shown = False
        toplevel.destroy()



class ToDoListScreen(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        tk.Label(self, text="To Do List", font=("Arial", 16, "bold"), fg="black").pack(pady=10)


class GoalsScreen(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        tk.Label(self, text="Goals", font=("Arial", 16, "bold"), fg="black").pack(pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("800x400")

        # Create a top bar for navigation
        nav_frame = tk.Frame(self, bg="black", height=40)
        nav_frame.pack(fill="x", side="top")

        # Create a container to hold the screens
        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        # Create a dictionary to store the screens
        self.screens = {}

        # Create the Schedule screen
        self.screens["Schedule"] = ScheduleScreen(container)

        # Create the Progress screen
        self.screens["Progress"] = ProgressScreen(container)

        # Create the To Do List screen
        self.screens["To Do List"] = ToDoListScreen(container)

        # Create the Goals screen
        self.screens["Goals"] = GoalsScreen(container)
        # Add black boxes around each title
        for screen_name in self.screens:
            box = tk.Frame(nav_frame, bg="black", width=100, height=30)
            box.pack(side="left", padx=10, pady=5)
            button = tk.Button(box, text=screen_name, font=("Arial", 12, "bold"), fg="white", bg="black", command=lambda name=screen_name: self.show_screen(name))
            button.pack(fill="both", expand=True)

        # Show the Schedule screen by default
        self.show_screen("Schedule")

        # Hide the Color Entry

    def show_screen(self, screen_name):
        # Hide all screens except the one specified
        for name, screen in self.screens.items():
            if name == screen_name:
                screen.pack(fill="both", expand=True)
            else:
                screen.pack_forget()

    def add_screen(self, screen_name, screen_frame):
        # Create a new screen with the given name and frame
        self.screens[screen_name] = screen_frame

        # Create a button for the new screen
        box = tk.Frame(self.nav_frame, bg="black", width=100, height=30)
        box.pack(side="left", padx=10, pady=5)
        button = tk.Button(box, text=screen_name, font=("Arial", 12, "bold"), fg="white", bg="black", command=lambda name=screen_name: self.show_screen(name))
        button.pack(fill="both", expand=True)


app = App()
app.mainloop()

# Create a new screen

