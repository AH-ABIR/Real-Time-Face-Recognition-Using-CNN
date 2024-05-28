import subprocess
import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import messagebox

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            text_to_speech("Please enter the subject name.")
            return
        
        directory = f"Attendance/{Subject}"
        filenames = glob(f"{directory}/{Subject}*.csv")
        if not filenames:
            messagebox.showinfo("Error", "No files found for this subject.")
            return
        
        dataframes = [pd.read_csv(filename) for filename in filenames]
        if not dataframes:
            messagebox.showinfo("Error", "Could not read any data from files.")
            return
        
        combined_df = dataframes[0]
        for df in dataframes[1:]:
            combined_df = pd.merge(combined_df, df, how="outer")
        
        combined_df.fillna(0, inplace=True)
        combined_df["Attendance"] = 0
        for i in range(len(combined_df)):
            combined_df["Attendance"].iloc[i]  = str(int(round(combined_df.iloc[i, 2:-1].mean() * 100)))+'%'
        combined_df.to_csv(f"{directory}/combined_attendance.csv", index=False)
        
        # Show results in a new window
        show_results(combined_df, Subject)

    def show_results(dataframe, Subject):
        result_window = tk.Tk()
        result_window.title(f"Attendance of {Subject}")
        result_window.configure(background="black")
        
        row_number = 0
        for index, row in dataframe.iterrows():
            for col_number, item in enumerate(row):
                label = tk.Label(result_window, text=item, width=10, height=1, fg="yellow", font=("times", 15, "bold"), bg="black", relief=tk.RIDGE)
                label.grid(row=row_number, column=col_number)
            row_number += 1
        result_window.mainloop()

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            # Ensure the path uses forward slashes and is correctly escaped or handled
            file_path = f"Attendance/{sub}"
            subprocess.run(['xdg-open', file_path])



    # Creating the main window
    subject = tk.Tk()
    subject.title("Subject Attendance")
    subject.geometry("580x320")  # Adjust the window size if needed
    subject.configure(background="#333333")  # A darker shade for professional look

    # Title label
    titl = tk.Label(subject, text="View Attendance", bg="#333333", fg="#00FF00", font=("Arial", 20))
    titl.place(x=50, y=20)

    # Entry for subject
    sub_label = tk.Label(subject, text="Enter Subject:", bg="#333333", fg="#FFFF00", font=("Times New Roman", 15))
    sub_label.place(x=50, y=100)

    tx = tk.Entry(subject, width=24, bd=3, bg="#222222", fg="#FFFF00", font=("Times", 18, "bold"))
    tx.place(x=200, y=100)

    # Buttons
    view_button = tk.Button(subject, text="View Attendance", command=calculate_attendance, bd=3, font=("Times New Roman", 15), bg="#222222", fg="#FFFF00")
    view_button.place(x=200, y=170)

    attf = tk.Button(subject, text="Check Sheets", command=Attf, bd=3, font=("Times New Roman", 15), bg="#222222", fg="#FFFF00", relief=tk.RIDGE)
    attf.place(x=400, y=170)

    subject.mainloop()

