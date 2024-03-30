import numpy as np
import tensorflow as tf
import keras
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
stat_df = pd.read_csv(dir_path + '/stat_train_features.csv')
mean_list = stat_df['mean'].to_list()
std_list = stat_df['std'].to_list()


def init_model(filename):
    model = keras.models.load_model(filename)
    return model


def scale_face_landmarks(face_landmarks):
    for i in range(len(face_landmarks)):
        face_landmarks[i] = (face_landmarks[i] - mean_list[i]) / std_list[i]

    return face_landmarks

def detect_emotions(model, landmarks):
    scaler = StandardScaler()

    face_landmarks = []
    for i in range(len(landmarks)):
        face_landmarks.append(landmarks[i].x)
        face_landmarks.append(landmarks[i].y)
        face_landmarks.append(landmarks[i].z)
    
    face_landmarks = scale_face_landmarks(face_landmarks)

    predicted_emotion = model.predict(np.array([face_landmarks,]))

    confidence_levels = {
        "Angry" : "Angry: " + str(round(predicted_emotion[0][0] * 100, 2)) + "%",
        "Happy" : "Happy: " + str(round(predicted_emotion[0][1] * 100, 2)) + "%",
        "Neutral" : "Neutral: " + str(round(predicted_emotion[0][2] * 100, 2)) + "%",
        "Sad" : "Sad: " + str(round(predicted_emotion[0][3] * 100, 2)) + "%"
    }

    return confidence_levels