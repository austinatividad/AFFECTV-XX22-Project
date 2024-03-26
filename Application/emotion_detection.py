import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import StandardScaler

def init_model(filename):
    model = keras.models.load_model(filename)
    return model

def detect_emotions(model, landmarks):

    face_landmarks = []
    print(landmarks)
    for i in range(len(landmarks)):
        face_landmarks.append(landmarks[i].x)
        face_landmarks.append(landmarks[i].y)
        face_landmarks.append(landmarks[i].z)
    
    predicted_emotion = model.predict(np.array([face_landmarks,]))

    confidence_levels = {
        "Angry" : "Angry: " + str(round(predicted_emotion[0][0] * 100, 2)) + "%",
        "Happy" : "Happy: " + str(round(predicted_emotion[0][1] * 100, 2)) + "%",
        "Neutral" : "Neutral: " + str(round(predicted_emotion[0][2] * 100, 2)) + "%",
        "Sad" : "Sad: " + str(round(predicted_emotion[0][3] * 100, 2)) + "%"
    }


    return confidence_levels