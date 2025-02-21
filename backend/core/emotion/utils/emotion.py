from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier(r'C:\Users\Mayank\Downloads\emotion-detection-main\emotion-detection-main\haarcascade_frontalface_default.xml')
classifier = load_model(r'C:\Users\Mayank\eeg_project\models\model.h5')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def detect_emotion_from_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    results = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]
            results.append({"face": (x, y, w, h), "emotion": label})
        else:
            results.append({"face": (x, y, w, h), "emotion": "No Face Detected"})

    return results
