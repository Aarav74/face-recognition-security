import cv2
import os

dataset_path = "dataset"
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

user_id = input("Enter user ID: ")
user_name = input("Enter user name: ")
user_folder = os.path.join(dataset_path, user_name)
if not os.path.exists(user_folder):
    os.makedirs(user_folder)

cap = cv2.VideoCapture(0)
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        
        face_img = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{user_folder}/face{count}.jpg", face_img)
        count += 1
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Collecting Face Data", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:  
        break

cap.release()
cv2.destroyAllWindows()
print(f"Collected {count} images for {user_name}.")