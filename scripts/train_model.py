import cv2
import os
import numpy as np
import json


def collect_data():
    faces = []
    labels = []
    label_dict = {} 
    current_label = 0  

    dataset_path = "dataset"
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                path = os.path.join(root, file)
                folder_name = os.path.basename(root)

                
                if folder_name not in label_dict:
                    label_dict[folder_name] = current_label
                    current_label += 1

                label = label_dict[folder_name]
                image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                faces.append(image)
                labels.append(label)

    return faces, labels, label_dict


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


faces, labels, label_dict = collect_data()


recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.train(faces, np.array(labels))


trainer_path = "trainer"
if not os.path.exists(trainer_path):
    os.makedirs(trainer_path)
recognizer.save(os.path.join(trainer_path, "trainer.yml"))


with open(os.path.join(trainer_path, "label_mapping.json"), "w") as f:
    json.dump(label_dict, f)

print("Training complete. Model saved as 'trainer.yml'.")
print("Label mapping saved as 'label_mapping.json'.")