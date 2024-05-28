import os
import cv2
import time
import datetime
import subprocess
import pandas as pd
import tkinter as tk
from tkinter import *
from tensorflow.keras.models import load_model

# Function to handle subject selection and attendance marking
def subjectChoose(studentdetail_path, attendance_path, model_path, haarcasecade_path, text_to_speech):
    # Function to take attendance
    df_students = pd.read_csv(studentdetail_path)
    def FillAttendance():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return

        try:
            model = load_model(model_path)
            model.summary()
        except:
            e = "Model not found, please train the model."
            Notifica.configure(text=e, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
            Notifica.place(x=20, y=250)
            text_to_speech(e)
            return

        facecasCade = cv2.CascadeClassifier(haarcasecade_path)
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        id_counts = {}  # Dictionary to count IDs
        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)
        start_time = time.time()
        while time.time() < start_time + 20:  # run for 20 seconds
            ret, frame = cap.read()
            if not ret:
                continue

            faces = facecasCade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (32, 32))
                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                gray = gray.reshape(-1, 32, 32, 1).astype('float32') / 255.0
                prediction = model.predict(gray, verbose=0)
                predicted_id = prediction.argmax()
                confidence = prediction[0, predicted_id]
                Subject = tx.get()
                if confidence > 0.3:  # Confidence threshold
                    id_counts[predicted_id] = id_counts.get(predicted_id, 0) + 1
                name = df_students.loc[df_students['Enrollment'] == predicted_id, 'Name'].values[0]

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f'Name: {name} Conf: {confidence:.2f}', (x, y - 10), font, 0.5, (0, 255, 0), 1)

            cv2.imshow('Filling Attendance...', frame)
            if cv2.waitKey(10) == 27:  # ESC key
                break

        cap.release()
        cv2.destroyAllWindows()

        # Determine the most frequent ID
        if id_counts:
            most_frequent_id = max(id_counts, key=id_counts.get)
            name = df_students.loc[df_students['Enrollment'] == most_frequent_id, 'Name'].values[0]
            m = f"Roll: {most_frequent_id} Name: {name}"
            attendance.loc[len(attendance)] = [most_frequent_id, name]
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            attendance[date] = 1
            Hour, Minute, Second = timeStamp.split(":")
            path = os.path.join(attendance_path, Subject)
            fileName = (
                f"{path}/"
                + Subject
                + "_"
                + date
                + "_"
                + Hour
                + "-"
                + Minute
                + "-"
                + Second
                + ".csv"
            )
            attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
            attendance.to_csv(fileName, index=False)
            print(attendance)

            Notifica.configure(text=m, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
            Notifica.place(x=20, y=250)
            text_to_speech(m)
        else:
            m = "No faces detected with sufficient confidence."
            Notifica.configure(text=m, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
            Notifica.place(x=20, y=250)
            text_to_speech(m)

    # Function to open attendance files
    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            file_path = os.path.join(attendance_path, sub)
            subprocess.run(['xdg-open', file_path])

    # GUI Setup
    subject = tk.Tk()
    subject.title("Subject Attendance")
    subject.geometry("580x320")
    subject.configure(background="#333333")

    titl = tk.Label(subject, text="Take Attendance", bg="#333333", fg="#00FF00", font=("Arial", 20))
    titl.place(x=50, y=20)

    sub_label = tk.Label(subject, text="Enter Subject:", bg="#333333", fg="#FFFF00", font=("Times New Roman", 15))
    sub_label.place(x=50, y=100)

    tx = tk.Entry(subject, width=24, bd=3, bg="#222222", fg="#FFFF00", font=("Times", 18, "bold"))
    tx.place(x=200, y=100)

    view_button = tk.Button(subject, text="Take Attendance", command=FillAttendance, bd=3, font=("Times New Roman", 15), bg="#222222", fg="#FFFF00")
    view_button.place(x=200, y=170)

    attf_button = tk.Button(subject, text="Check Sheets", command=Attf, bd=3, font=("Times New Roman", 15), bg="#222222", fg="#FFFF00")
    attf_button.place(x=400, y=170)

    Notifica = tk.Label(subject, bg="yellow", fg="black", width=33, height=2, font=("Times", 15, "bold"))
    subject.mainloop()
