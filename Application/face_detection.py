
from mediapipe import solutions, tasks, ImageFormat, Image
from mediapipe.framework.formats import landmark_pb2
import numpy as np


def draw_landmarks_on_image_simplified(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_LIPS,
        landmark_drawing_spec=None,
        connection_drawing_spec=solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_LEFT_EYEBROW,
        landmark_drawing_spec=None,
        connection_drawing_spec=solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_RIGHT_EYEBROW,
        landmark_drawing_spec=None,
        connection_drawing_spec=solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_NOSE,
        landmark_drawing_spec=None,
        connection_drawing_spec=solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image

def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image

def init_model(filepath):
    BaseOptions = tasks.BaseOptions
    FaceLandmarker = tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = tasks.vision.FaceLandmarkerOptions

    base_options = BaseOptions(model_asset_path=filepath)
    options = FaceLandmarkerOptions(base_options=base_options, num_faces=1)

    #Test the model
    detector2 = FaceLandmarker.create_from_options(options)

    return detector2

def detect_faces(detector, cv2_image_data, fullMask):
    image = Image(image_format=ImageFormat.SRGB, data=cv2_image_data)
    detection_result = detector.detect(image) #this is the line
    
    if fullMask:
       return detection_result, draw_landmarks_on_image(image.numpy_view(), detection_result)
    else:
        return detection_result, draw_landmarks_on_image_simplified(image.numpy_view(), detection_result)