import numpy as np
from keras import models

MASK_MODE_FULL = 0
MASK_MODE_SIMPLIFIED = 1
MASK_MODE_LEFT = 2

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

left_face_landmarks_mid = [151, 9, 8, 168, 6, 197, 195, 5, 4, 1, 19, 94, 2, 164, 0, 11, 12, 13, 14, 15, 16, 17, 18, 200, 199, 175]
left_face_landmarks_lips = [37, 39, 40, 72, 73, 74, 38, 41, 42, 82, 81, 80, 185, 184, 183, 191, 61, 76, 67, 78, 95, 88, 178, 87, 96, 89, 179, 86, 77, 90, 180, 85, 146, 91, 181, 84]
left_face_left_eye = [33,246,161,160,159,158,157,173,133,155,154,153,145,144,163,7]
left_face_left_eyebrow = [70,63,105,66,107,55,65,52,53,46]
left_face_border = [10, 109, 67, 103, 54, 21, 162, 127, 237, 137, 93, 177, 132, 215, 58, 172, 136, 150, 149, 176, 148, 152]
left_face_nose_cluster = [45, 220, 115, 102, 129, 48, 218, 219, 64, 235, 166, 79, 237, 59, 239, 98, 240, 75, 239, 44, 60, 99, 97, 238, 20, 241, 242, 125, 141]
left_face_upper = [108, 69, 104, 68, 71, 139, 156, 124, 225, 224, 223, 221, 221, 193, 189, 190, 56, 28, 27, 29, 30, 247, 113, 130, 25, 110, 24, 23, 22, 26, 112, 243, 244, 245, 233, 232, 231, 230, 229, 228, 31, 35, 122, 188, 128, 121, 120, 100, 47, 114, 196, 174, 217, 126, 142, 209, 198, 236, 3, 131, 134, 51, 34, 143, 116, 111, 117, 118, 119, 101, 36, 50, 123]
left_face_lower = [205, 206, 203, 92, 165, 167, 147, 187, 213, 207, 192, 216, 186, 138, 214, 212, 57, 135, 210, 202, 43, 169, 106, 204, 211, 170, 182, 194, 32, 140, 83, 201, 208, 171]

combined_points_left = []
combined_points_left.extend(left_face_landmarks_mid)
combined_points_left.extend(left_face_landmarks_lips)
combined_points_left.extend(left_face_left_eye)
combined_points_left.extend(left_face_left_eyebrow)
combined_points_left.extend(left_face_border)
combined_points_left.extend(left_face_nose_cluster)
combined_points_left.extend(left_face_upper)
combined_points_left.extend(left_face_lower)


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

def get_left_landmarks(landmarks):
    new_landmarks = [landmarks[i] for i in combined_points_left]
    return new_landmarks


def detect_emotions(model, landmarks, stat_full, stat_left, stat_simp, maskMode):
    if maskMode == MASK_MODE_FULL:
        mean_list = stat_full['mean'].to_list()
        std_list = stat_full['std'].to_list()
    elif maskMode == MASK_MODE_LEFT:
        mean_list = stat_left['mean'].to_list()
        std_list = stat_left['std'].to_list()
        landmarks = get_left_landmarks(landmarks)
    elif maskMode == MASK_MODE_SIMPLIFIED:
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