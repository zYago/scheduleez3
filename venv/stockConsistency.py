import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt
from tkinter import simpledialog


class stockConsistency:


    # Create or read the dataframe from the CSV file
    def __init__(self, parent):
        self.filename = "C:\\Users\\yagof\\IdeaProjects\\scheduleez\\venv\\colorLog\\color_log.csv"
        try:
            df = pd.read_csv(self.filename)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["date", "color", "value", "balance"])

        self.df = df
        self.parent = parent
        self.parent.title("P&L Graph")


    # Add a label and a button for the Green color
        self.today = pd.Timestamp.now().date()

        if not df.empty and df["date"].iloc[-1] == self.today:
            self.show_graph()
            self.parent.destroy()

        else:
            green_label = Label(self.parent, text="Green")
            green_label.grid(row=0, column=0)


            def add_green():
                balance = self.ask_for_balance()
                if not df.empty and df["date"].iloc[-1] == self.today:
                    df.loc[len(df)-1, "balance"] = balance
                else:
                    if not df.empty:
                        prev_value = df['value'].iloc[-1]
                        new_value = prev_value + 1
                    else:
                        new_value = 1

                    df.loc[len(df)] = [self.today, "Green", new_value, balance]

                df.to_csv(self.filename, index=False)

                self.show_graph()
                self.parent.destroy()
            last_entry = df["date"].iloc[-1]
            print(last_entry)
            print(self.today.strftime("%Y-%m-%d"))

            if (last_entry == self.today.strftime("%Y-%m-%d")):
                self.green_button = Button(self.parent, text="Add", command=add_green, state=DISABLED)
                self.green_button.grid(row=0, column=1)
            else:
                self.green_button = Button(self.parent, text="Add", command=add_green)
                self.green_button.grid(row=0, column=1)


            # Add a label and a button for the Red color
            red_label = Label(self.parent, text="Red")
            red_label.grid(row=1, column=0)

            def add_red():
                balance = self.ask_for_balance()
                if not df.empty and df["date"].iloc[-1] == self.today:
                    df.loc[len(df)-1, "balance"] = balance
                else:
                    if not df.empty:
                        prev_value = df['value'].iloc[-1]
                        new_value = prev_value - 1
                    else:
                        new_value = -1

                    df.loc[len(df)] = [today, "Red", new_value, balance]

                df.to_csv(filename, index=False)

                self.show_graph()
                self.parent.destroy()
            if (last_entry == self.today.strftime("%Y-%m-%d")):
                self.red_button = Button(self.parent, text="Add", command=add_red, state=DISABLED)
                self.red_button.grid(row=1, column=1)
                self.graph_button = Button(self.parent, text="Show Graph", command=lambda: self.show_graph())
                self.graph_button.grid(row=2, column=0, columnspan=2)
            else:
                self.red_button = Button(self.parent, text="Add", command=add_red)
                self.red_button.grid(row=1, column=1)
                # Add a button to show the graph
                self.graph_button = Button(self.parent, text="Show Graph", command=lambda: self.show_graph())
                self.graph_button.grid(row=2, column=0, columnspan=2)



    def show_graph(self):

        def on_close(event):
            plt.close(fig)
        # Read the data from the CSV file
        df = pd.read_csv(self.filename)

        # Plot the data
        fig = plt.figure()
        fig.canvas.mpl_connect('close_event', on_close)
        plt.plot(df["date"], df["value"], color="purple")
        plt.xlabel("Date", fontsize=8)
        plt.ylabel("Win or Loss", fontsize=16, fontweight="bold")
        plt.grid()
        plt.show()


    def ask_for_balance(self):
        balance = simpledialog.askinteger("Balance", "Enter the balance:")
        return balance if balance is not None else 0
        self.graph_button.config(command=self.show_graph)



        # Start the main event loop
if __name__ == "__main__":
    root = Tk()
    app = stockConsistency(root)
    root.mainloop()
