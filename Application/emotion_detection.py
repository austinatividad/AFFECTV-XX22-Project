import numpy as np
from keras import models

left_eyebrow = [70,63,105,66,107,55,65,52,53,46] #Seen
right_eyebrow = [300,293,334,296,336,285,295,282,283,276] #Seen
left_eye = [33,246,161,160,159,158,157,173,133,155,154,153,145,144,163,7] #Seen
right_eye =  [263,466,388,387,386,385,384,398,362,382,381,380,374,373,390,249] #Seen
inner_lip = [78,191,80,81,82,13,312,311,310,415,308,324,318,402,317,14,87,178,88,95] #Seen
outer_lip =  [61,185,40,39,37,0,267,269,270,409,291,375,321,405,314,17,84,181,91,146] #Seen
face_boundary = [10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109]
left_iris = [468,469,470,471,472] #Seen
right_iris = [473,474,475,476,477] #Seen
nose = [64,4,294]

combined_points = []
combined_points.extend(left_eyebrow)
combined_points.extend(right_eyebrow)
combined_points.extend(left_eye)
combined_points.extend(right_eye)
combined_points.extend(inner_lip)
combined_points.extend(outer_lip)
combined_points.extend(face_boundary)
combined_points.extend(left_iris)
combined_points.extend(right_iris)
combined_points.extend(nose)

def init_model(filename):
    model = models.load_model(filename)
    return model


def scale_face_landmarks(face_landmarks, mean_list, std_list):
    for i in range(len(face_landmarks)):
        face_landmarks[i] = (face_landmarks[i] - mean_list[i]) / std_list[i]

    return face_landmarks

def simplify_landmarks(landmarks):
    new_landmarks = [landmarks[i] for i in combined_points]
    return new_landmarks


def detect_emotions(model, landmarks, stat_full, stat_simp, fullMask):
    if fullMask:
        mean_list = stat_full['mean'].to_list()
        std_list = stat_full['std'].to_list()
    else:
        mean_list = stat_simp['mean'].to_list()
        std_list = stat_simp['std'].to_list()
        landmarks = simplify_landmarks(landmarks)

    face_landmarks = []
    for i in range(len(landmarks)):
        face_landmarks.append(landmarks[i].x)
        face_landmarks.append(landmarks[i].y)
        face_landmarks.append(landmarks[i].z)
    
    face_landmarks = scale_face_landmarks(face_landmarks, mean_list, std_list)

    predicted_emotion = model.predict(np.array([face_landmarks,]))

    confidence_levels = {
        "Angry" : round(predicted_emotion[0][0] * 100, 2),
        "Happy" : round(predicted_emotion[0][1] * 100, 2),
        "Neutral" : round(predicted_emotion[0][2] * 100, 2),
        "Sad" : round(predicted_emotion[0][3] * 100, 2)
    }

    return confidence_levels