import pyttsx3
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

# project module
import showAttendance
import takeImage
import trainImage
import automaticAttendance

model_path = ("weights/trained_model.h5")
studentdetail_path = ("StudentDetails/studentdetails.csv")
haarcasecade_path = "weights/haarcascade_frontalface_default.xml"
trainimage_path = "dataset"
attendance_path = "Attendance"
filepath = "dataset/labels.txt"


def text_to_speech(user_text):
    engine = pyttsx3.init("dummy")
    engine.say(user_text)
    engine.runAndWait()

window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="black")

# to destroy screen
def del_sc1():
    sc1.destroy()

# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="black")
    sc1.resizable(0, 0)
    tk.Label(sc1, text="Enrollment & Name required!!!", fg="yellow", bg="black", font=("times", 20, " bold ")).pack()
    tk.Button(sc1, text="OK", command=del_sc1, fg="yellow", bg="black", width=9, height=1, activebackground="Red", font=("times", 20, " bold ")).place(x=110, y=50)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


a = tk.Label(window, text="Welcome to the Face Recognition Based\nAttendance Management System", bg="black", fg="yellow", bd=10, font=("arial", 35))
a.pack()

ri = Image.open("UI_Image/register.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r)
label1.image = r
label1.place(x=100, y=200)

ai = Image.open("UI_Image/attendance.png")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a)
label2.image = a
label2.place(x=980, y=200)

vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v)
label3.image = v
label3.place(x=560, y=200)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#333333")
    ImageUI.resizable(0, 0)

    # image and title
    titl = tk.Label(ImageUI, text="Register Your Face", bg="#333333", fg="#00FF00", font=("Arial", 20))
    titl.place(x=270, y=12)

    # heading
    a = tk.Label(ImageUI, text="Enter the details", bg="#333333", fg="yellow", bd=10, font=("arial", 20))
    a.place(x=280, y=75)

    # ER no
    lbl1 = tk.Label(ImageUI, text="Enrollment No:", bg="#333333", fg="#FFFF00", font=("Times New Roman", 15))
    lbl1.place(x=120, y=130)

    txt1 = tk.Entry(ImageUI, width=24, bd=3, validate="key", bg="#222222", fg="#FFFF00", font=("Times", 18, "bold"), relief=RIDGE)
    txt1.place(x=290, y=130)
    
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(ImageUI, text="Name:", bg="#333333", fg="#FFFF00", font=("Times New Roman", 15))
    lbl2.place(x=120, y=200)

    txt2 = tk.Entry(ImageUI, width=24, bd=3, bg="#222222", fg="#FFFF00", font=("Times", 18, "bold"), relief=RIDGE)
    txt2.place(x=290, y=200)

    # notification
    lbl3 = tk.Label(ImageUI, text="Notification:", bg="#333333", fg="#FFFF00", font=("Times New Roman", 15))
    lbl3.place(x=120, y=270)

    message = tk.Label(ImageUI, text="", width=24, bd=5, bg="#222222", fg="#FFFF00", font=("Times", 18, "bold"), relief=RIDGE)
    message.place(x=290, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(l1, l2, haarcasecade_path, filepath, message, text_to_speech)
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button( ImageUI, text="Take Image", command=take_image, bd=10, font=("times new roman", 16), bg="black", fg="yellow", width=12, relief=RIDGE)
    takeImg.place(x=200, y=350)

    def train_image():
        trainImage.TrainImage(trainimage_path, model_path, message, text_to_speech)

    # train Image function call
    trainImg = tk.Button( ImageUI, text="Train Image", command=train_image, bd=10, font=("times new roman", 16), bg="black", fg="yellow", width=12, relief=RIDGE)
    trainImg.place(x=430, y=350)

def automatic_attedance():
    automaticAttendance.subjectChoose(studentdetail_path, attendance_path, model_path, haarcasecade_path, text_to_speech)

def view_attendance():
    showAttendance.subjectchoose(text_to_speech)

# UI Configuration
style = {"bg": "#1f1f1f", "fg": "#ffcc00", "font": ("times new roman", 16), "bd": 10, "height": 2, "width": 17, "relief": RIDGE}

button_register = Button(window, text="Register a new student", command=TakeImageUI, **style)
button_register.place(x=100, y=450)

button_attendance = Button(window, text="Take Attendance", command=automatic_attedance, **style)
button_attendance.place(x=560, y=450)

button_view = Button(window, text="View Attendance", command=view_attendance, **style)
button_view.place(x=980, y=450)

button_exit = Button(window, text="EXIT", bd=10, command=quit, font=("times new roman", 16), bg="black", fg="red", height=2, width=17)
button_exit.place(x=560, y=590)

window.mainloop()
