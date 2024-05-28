import cv2
import os
import time
import csv

def TakeImage(face_id, face_name, haarcasecade_path, file_path, message, text_to_speech):
    if (face_id == "") and (face_name==""):
        t='Please Enter the your Enrollment Number and Name.'
    elif face_id=='':
        t='Please Enter the your Enrollment Number.'
    elif face_name == "":
        t='Please Enter the your Name.'
    else:
        try:
            Enrollment = face_id
            Name = face_name
            # Check if the file exists
            file_exists = os.path.exists(file_path)
            if not os.path.exists('dataset'):
                os.mkdir('dataset')

            # Open the file in append mode (creates the file if it doesn't exist)
            with open(file_path, 'a') as file:
                # Add a newline character if the file is new
                if file_exists:
                    file.write('\n')
                
                # Append text to the file
                text_to_append = face_name
                file.write(text_to_append)

            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
            csvFile.close()

            # Variables for FPS calculation
            frame_count = 0
            start_time = time.time()
            fps = 0  # Initialize fps variable

            cam = cv2.VideoCapture(0)
            face_detector = cv2.CascadeClassifier(haarcasecade_path)
            count = 0

            while(True):
                ret, img = cam.read()
                img = cv2.flip(img, 1) # flip video image vertically
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)

                for (x,y,w,h) in faces:

                    cv2.rectangle(img, (x,y), (x+w+50,y+h+50), (255,0,0), 2)     

                    # Save the captured image into the datasets folder
                    gray = gray[y:y+h,x:x+w]

                    try:
                        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg",gray )
                    except Exception as e:
                        print(e)
                        print(gray)
                        continue


                    # Calculate FPS and display it on the image
                    frame_count += 1
                    if frame_count >= 1:  # Calculate FPS every 30 frames (adjust as needed)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        fps = frame_count / elapsed_time
                        frame_count = 0
                        start_time = time.time()

                    #Add FPS counter
                    cv2.putText(img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    #Add number of images of face captures
                    text_position = (img.shape[1] - 300, 30)
                    cv2.putText(img, f"Img Captured: {count}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    cv2.imshow('image', img)
                    count += 1

                k = cv2.waitKey(20) & 0xff # Press 'ESC' for exiting video
                if k == 27:
                    break
                elif count >= 100: # Take 100 face sample and stop video
                    break

            # Do a bit of cleanup
            print("\n [INFO] Exiting Program and cleanup stuff")
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ER No:" + Enrollment + " Name:" + Name
            message.configure(text=res)
            text_to_speech(res)
        except FileExistsError as F:
            F = "Student Data already exists"
            text_to_speech(F)

