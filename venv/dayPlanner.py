import pandas as pd
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
import os

class DayPlanner:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Day Planner")

        # Create a frame for the time labels
        self.time_frame = ttk.Frame(self.parent)
        self.time_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create buttons for every hour
        self.buttons = []
        for hour in range(24):
            if hour < 5:
                continue
            button = ttk.Button(self.time_frame, text=f"{hour:02d}:00", command=lambda h=hour: self.filter_boxes(h))
            button.pack(side=tk.TOP, pady=3, anchor=tk.NW)
            self.buttons.append(button)

        # Create a canvas with a scrollbar for the entry boxes
        self.canvas = tk.Canvas(self.parent, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.parent, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame to hold the entry boxes
        self.box_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.box_frame, anchor=tk.NW)

        # Create the entry boxes and labels for every 5-minute interval
        self.boxes = []
        for i in range(1440 // 5):
            time = datetime.time(hour=i // 12, minute=(i % 12) * 5)
            box = ttk.Entry(self.box_frame, width=40)
            label = ttk.Label(self.box_frame, text=time.strftime("%I:%M %p"))
            self.boxes.append((time, box, label))
            # '%H:%M'

        # Filter the boxes to display only those for the current hour
        self.current_hour = datetime.datetime.now().hour
        self.filter_boxes(self.current_hour)

        # Resize the canvas scrollable area when the window is resized
        def resize_canvas(event):
            self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

        self.parent.bind("<Configure>", resize_canvas)

        # Add a "Save" button
        self.save_button = ttk.Button(self.parent, text="Save", command=self.save_boxes)
        self.save_button.pack(side=tk.BOTTOM)

        # Add a "Load" button
        self.load_button = ttk.Button(self.parent, text="Load", command=self.load_boxes)
        self.load_button.pack(side=tk.BOTTOM, pady=5)

    def filter_boxes(self, hour):
        self.current_hour = hour
        for i, (time, box, label) in enumerate(self.boxes):
            if time.hour == hour:
                box.grid(row=i, column=1, sticky="nsew", padx=5, pady=5)
                label.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            else:
                box.grid_forget()
                label.grid_forget()
        if self.current_hour >= 5:
            self.buttons[self.current_hour - 5].focus_set()
        else:
            self.buttons[0].focus_set()

    def save_boxes(self):
        # Create a dictionary to store the data in the boxes
        data = []
        for time, box, label in self.boxes:
            if time < datetime.time(hour=5):
                continue
            data.append((time.strftime('%H:%M'), box.get()))

        date_str = simpledialog.askstring("Load day", "Enter the date (MM/DD/YYYY):")
        try:
            date = datetime.datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            tk.messagebox.showerror("Invalid date", "Please enter a valid date (MM/DD/YYYY).")
            return

        # Convert the dictionary to a pandas DataFrame and save it to a CSV file
        df = pd.DataFrame(data, columns=['Time', 'Text'])
        filename = date.strftime('Day-Plan-%m-%d-%Y.csv')
        df.to_csv(f"C:\\Users\\yagof\\IdeaProjects\\scheduleez\\venv\\dayPlans\\{filename}", index=False)
        print(df)


    def load_boxes(self):
        # Ask the user for the date to load
        date_str = simpledialog.askstring("Load day", "Enter the date (MM/DD/YYYY):")
        try:
            date = datetime.datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            tk.messagebox.showerror("Invalid date", "Please enter a valid date (MM/DD/YYYY).")
            return

        # Check if there is a CSV file for that day
        filename = date.strftime('Day-Plan-%m-%d-%Y.csv')
        if not os.path.isfile(f"C:\\Users\\yagof\\IdeaProjects\\scheduleez\\venv\\dayPlans\\{filename}"):
            tk.messagebox.showerror("File not found", f"No file found for {date_str}.")
            return

        # Load the data from the CSV file
        df = pd.read_csv(f"C:\\Users\\yagof\\IdeaProjects\\scheduleez\\venv\\dayPlans\\{filename}")

        # Fill the entry boxes with the loaded data
        for time, box, label in self.boxes:
            if time < datetime.time(hour=5):
                continue
            row = df.loc[df['Time'] == time.strftime('%H:%M')]
            if not row.empty:
                box.delete(0, tk.END)
                box.insert(0, row.iloc[0]['Text'])

# Create the main window and start the event loop
if __name__ == "__main__":
    root = tk.Tk()
    app = DayPlanner(root)
    root.mainloop()