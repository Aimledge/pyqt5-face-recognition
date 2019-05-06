"""
Copyright (C) 2018, AIMLedge Pte, Ltd.
All rights reserved.

"""
import abc
import logging
import cv2

logger = logging.getLogger('Face_Rec')


# Face recognizer interface. Different algorithm implementations will
# implement this interface. We are using Strategy design pattern here.
class FaceRecognizer(metaclass=abc.ABCMeta):
  def __init__(self):
    pass

  @abc.abstractmethod
  def create_face_registry(self, registry_name):
    """

    :param registry_name: Face registry name
    :return: Created face registry name
    """

  @abc.abstractmethod
  def delete_face_registry(self, registry_name):
    """

    :param registry_name: Face registry name to delete
    :return: Deleted registry name if there was such registry else raises
    ValueError
    """

  @abc.abstractmethod
  def get_active_face_registry(self):
    """

    :return: Returns the face registry name if any that is being used for
    face recognition. Returns None if no registry is added to the recognizer.
    """
    pass

  @abc.abstractmethod
  def set_active_face_registry(self, registry_name):
    """

    :param registry_name: Registry name to use for face recognition from now on
    :return: Active face registry if the operation is successful else raises
    Exception
    """
    pass

  @abc.abstractmethod
  def list_face_registries(self):
    """

    :return: List of face registries present
    """
    pass

  @abc.abstractmethod
  def face_registry_details(self, registry_name):
    """

    :param registry_name: Registry name
    :return: A generator function that returns (face_id, face_name,
    face_image) that are registered in this registry.
    """
    pass

  @abc.abstractmethod
  def register_face(self, registry_name, image, name):
    """

    :param registry_name: Face registry name to registry face.
    :param image: A of np.ndarray representing BGR image or image file.
    :param name: Name of the person present in the image. If the image
    contains more than one face, then the name must be of the largest face
    present.
    :return: Image ID for the registered face.
    """
    pass

  @abc.abstractmethod
  def recognize_faces(self, image):
    """

    :param image: A single np.ndarray representing the target image in the
    BGR format OR an image file.
    :return: A list of dict of the form {'face_id': str, 'face_name': str,
    'box': [xmin, ymin, xmax, ymax], 'detection_score': float,
    'recognition_score': float }
    """
    pass

  @abc.abstractmethod
  def deregister_face(self, registry_name, face_id):
    """

    :param registry_name: Registry name from which to deregister face
    :param face_id: Face ID to deregister
    :return: de-registered (face_id, face_name) if the operation is successful
    else (None, None)
    """
    pass

  @abc.abstractmethod
  def get_face_name(self, registry_name, face_id):
    """

    :param registry_name: Face registry name
    :param face_id: Face ID for which face name to be given
    :return: Face name if the face_id is registered else None
    """
    pass

  @staticmethod
  def draw_face_recognitions(image, recognition_data):
    """

    :param image: np.ndarray containing BGR image
    :param recognition_data: Data returned by self.recognize_faces
    :return:
    """
    color = (255, 0, 0)
    for face_data in recognition_data:
      box = face_data['box']
      if face_data['face_id'] is None:
        label = '{:s}'.format(face_data['face_name'])
      else:
        label = '{:s} : {:d}%'.format(face_data['face_name'],
                                      int(face_data['recognition_score']))
      c1 = (int(box[0]), int(box[1]))
      c2 = (int(box[2]), int(box[3]))
      cv2.rectangle(image, c1, c2, color, thickness=2)
      text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 1)[0]

      c2 = c1[0] + text_size[0] + 10, c1[1] + text_size[1] + 5
      cv2.rectangle(image, c1, c2, color, -1)
      cv2.putText(image, label, (c1[0], c1[1] + text_size[1] + 10),
                  cv2.FONT_HERSHEY_PLAIN, 2, [225, 255, 255], 1)
