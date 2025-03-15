import cv2
import os
import serial
import time


arduino = serial.Serial('COM5', 9600) 
time.sleep(2)  


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("C:/Users/aarav/Desktop/face recognition security/trainer/trainer.yml")


folder_path = "C:/Users/aarav/Desktop/face recognition security/SecureFolder"

def unlock_folder():
    print("Folder unlocked!")
    os.startfile(folder_path)
    arduino.write(b'B') 

def lock_folder():
    print("Folder locked!")
    arduino.write(b'O') 

def wrong_face_detected():
    print("Wrong face detected!")
    arduino.write(b'R') 

def detect_face():
    cap = cv2.VideoCapture(0)  
    while True:
        ret, frame = cap.read()
        if not ret:
            break

       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < 70:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Authenticated", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                unlock_folder()
                return True
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                wrong_face_detected()

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

def main():
    while True:
       
        distance = arduino.readline().decode().strip()
        if distance:
            distance = int(distance)
            print(f"Distance: {distance} cm")

           
            if distance <= 50:
                print("Person detected. Starting face recognition...")
                if detect_face():
                    break  
            else:
                lock_folder()

if __name__ == "__main__":
    main()