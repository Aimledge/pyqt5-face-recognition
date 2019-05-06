"""
Copyright (C) 2018, AIMLedge Pte, Ltd.
All rights reserved.

"""

import pickle
import os
import face_recognition
import cv2
import numpy as np
from face_recognizer import FaceRecognizer, logger
from scipy.spatial import distance

FACE_REGISTRY_PATH = os.path.join(os.path.expanduser('~'),
                                  '.config/face-recognition')


class EdgeFaceRecognizer(FaceRecognizer):
  def __init__(self):
    logger.info('Creating edge face recognizer.')
    self._registry_faces = []
    self._registry_face_names = []
    self._registry_face_ids = []
    self._registry_face_encodings = []
    self._image_scale = 1.0
    self._num_upsamples = 2
    self._face_detector_type = 'cnn'   # hog or 'cnn'
    self._matching_thr = 0.1
    if not os.path.exists(FACE_REGISTRY_PATH):
      logger.info('Creating face registry at {}'.format(FACE_REGISTRY_PATH))
      os.makedirs(FACE_REGISTRY_PATH)
    self._face_registries = self.list_face_registries()
    self._active_face_registry = None

  def create_face_registry(self, registry_name):
    registry_path = self._get_face_registry_path(registry_name)
    if os.path.exists(registry_path):
      logger.info('Face registry already present. Not creating again')
    else:
      self._face_registries.append(registry_name)
      open(registry_path, 'w').close()
    return registry_name

  def delete_face_registry(self, registry_name):
    if registry_name not in self._face_registries:
      logger.warning('Looks like there is no such registry to delete.'.format(
        registry_name))
      raise ValueError('No such face registry {}'.format(registry_name))
    else:
      registry_path = self._get_face_registry_path(registry_name)
      os.remove(registry_path)
      if registry_name == self._active_face_registry:
        self._registry_face_names = []
        self._registry_faces = []
        self._registry_face_ids = []
        self._registry_face_encodings = []
        self._active_face_registry = None
      logger.info('Removed face registry {}'.format(registry_name))
      return registry_name

  def get_active_face_registry(self):
    return self._active_face_registry

  def set_active_face_registry(self, registry_name):
    if registry_name not in self._face_registries:
      raise ValueError('Face registry not found {}'.format(registry_name))
    # Nothing to do
    logger.info('Setting active face registry to {}'.format(registry_name))
    if self._active_face_registry == registry_name:
      return registry_name
    self._load_face_registry(registry_name)
    self._active_face_registry = registry_name
    return self._active_face_registry

  def list_face_registries(self):
    registry_names = []
    for reg_path in os.listdir(FACE_REGISTRY_PATH):
      file_ext = os.path.basename(reg_path).split('.')[-1]
      if file_ext == 'pkl':
        registry_names.append(os.path.basename(reg_path).split('.')[0])
    return registry_names

  def face_registry_details(self, registry_name):
    if registry_name != self._active_face_registry:
      raise NotImplementedError('Only able to give active face registry')
    num_faces = len(self._registry_face_ids)
    for idx in range(num_faces):
      yield self._registry_face_ids[idx], self._registry_face_names[idx], \
            self._registry_faces[idx]

  def register_face(self, registry_name, image, name):
    if registry_name not in self._face_registries:
      raise ValueError('No such face registry {}'.format(registry_name))
    if isinstance(image, str):
      image = face_recognition.load_image_file(image)

    face_boxes = face_recognition.face_locations(
      image, number_of_times_to_upsample=self._num_upsamples, model='cnn')
    if len(face_boxes) == 0:
      logger.warning('No faces found in the image')
      return None
    elif len(face_boxes) == 1:
      target_face_box = face_boxes[0]
      logger.info('Found one face in the image {}'.format(target_face_box))
    else:
      target_face_box = EdgeFaceRecognizer._get_largest_face(face_boxes)
      logger.info('Found multiple faces in the image. Taking the largest one {}'
                  ''.format(target_face_box))

    face_crop = image[target_face_box[0]:target_face_box[2],
                target_face_box[3]:target_face_box[1], :]
    encoding = face_recognition.face_encodings(image,
                                               known_face_locations=[target_face_box])
    new_face_id = self._get_new_face_id()

    if registry_name != self._active_face_registry:
      active_reg = self._active_face_registry
      self._load_face_registry(registry_name)
      assert registry_name == self._active_face_registry
    self._registry_faces.append(face_crop)
    self._registry_face_names.append(name)
    assert len(encoding) == 1
    self._registry_face_encodings.append(encoding[0])
    self._registry_face_ids.append(new_face_id)
    self._save_active_face_registry()

    # Restore active registry
    if registry_name != self._active_face_registry:
      self._load_face_registry(active_reg)

    return new_face_id

  def recognize_faces(self, image):
    resized_image = cv2.resize(image, (0, 0), fx=self._image_scale,
                               fy=self._image_scale)
    resized_image = resized_image[:, :, ::-1]
    # Returned face locations are [top(y1), right(x2), bottom(y2), left(x1)]
    face_locations = face_recognition.face_locations(
      resized_image, number_of_times_to_upsample=self._num_upsamples,
      model=self._face_detector_type)
    if len(face_locations) == 0:
      return []
    face_encodings = face_recognition.face_encodings(resized_image,
                                                     face_locations)
    face_encodings = np.array(face_encodings)
    # rescale face boxes and re-arrange the points in the (x1, x2, y1,
    # y2) order.
    detected_face_ids, detected_face_names, recognition_scores = self._match(
      face_encodings)
    face_locations = (np.array(face_locations) / self._image_scale).astype(
      np.int32)
    if face_locations.shape[0] > 0:
      face_locations[:, [0, 1, 2, 3]] = face_locations[:, [3, 0, 1, 2]]

    face_locations = list(map(tuple, face_locations))
    output = []
    for i in range(len(detected_face_names)):
      output.append({'face_id': detected_face_ids[i],
                     'face_name': detected_face_names[i],
                     'box': face_locations[i],
                     'detection_score': 1.0,
                     'recognition_score': recognition_scores[i]
                     }
                    )
    return output

  def deregister_face(self, registry_name, face_id):
    raise NotImplementedError('Feature not implemented.')

  def get_face_name(self, registry_name, face_id):
    if registry_name != self._active_face_registry:
      raise ValueError('Registry must be active in order to get name')
    if face_id in self._registry_face_ids:
      return self._registry_face_names[self._registry_face_ids.index(face_id)]
    else:
      raise ValueError('No such face ID')

  def _find_best_match(self, face_encoding):
    found = False
    norm_dist = face_recognition.face_distance(self._registry_face_encodings,
                                               face_encoding)

    closest_match_idx = np.argmin(norm_dist)
    closest_match_conf = norm_dist[closest_match_idx]
    if closest_match_conf <= self._matching_thr:
      found = True
    return found, closest_match_idx, closest_match_conf

  def _match(self, face_encodings):
    assert len(self._registry_face_encodings) > 0
    gallary = np.array(self._registry_face_encodings)
    dist_mat = distance.cdist(gallary, face_encodings, metric='cosine')
    rows = dist_mat.min(axis=1).argsort()
    cols = dist_mat.argmin(axis=1)[rows]

    used_rows = set()
    used_cols = set()
    all_face_ids = [-1 for i in range(len(face_encodings))]
    all_face_names = ['Unknown' for i in range(len(face_encodings))]
    all_scores = [0 for i in range(len(face_encodings))]
    for (row, col) in zip(rows, cols):
      if row in used_rows or col in used_cols:
        continue
      if dist_mat[row, col] > self._matching_thr:
        continue
      all_face_ids[col] = self._registry_face_ids[row]
      all_face_names[col] = self._registry_face_names[row]
      all_scores[col] = (1 - dist_mat[row, col]) * 100
      used_rows.add(row)
      used_cols.add(col)
    return all_face_ids, all_face_names, all_scores

  def _get_face_registry_path(self, registry_name):
    """

    :param registry_name:
    :return:
    """
    return os.path.join(FACE_REGISTRY_PATH, registry_name + '.pkl')

  def _load_face_registry(self, registry_name):
    reg_path = self._get_face_registry_path(registry_name)
    if os.path.exists(reg_path):
      with open(reg_path, 'rb') as f:
        try:
          data = pickle.load(f)
          self._registry_face_encodings = data['face_encodings']
          self._registry_faces = data['face_images']
          self._registry_face_names = data['face_names']
          self._registry_face_ids = data['face_ids']
          self._active_face_registry = registry_name
          logger.info('Loaded face registry {}. Set it as active face '
                      'registry'.format(registry_name))
        except Exception as e:
          logger.warning('Falied to load the face registry {}'.format(e))

  def _save_active_face_registry(self):
    registry_path = self._get_face_registry_path(self._active_face_registry)
    with open(registry_path, 'wb') as f:
      pickle.dump({'face_ids': self._registry_face_ids,
                   'face_names': self._registry_face_names,
                   'face_images': self._registry_faces,
                   'face_encodings': self._registry_face_encodings
                   }, f)
      logger.info('Saved active face registry')

  def _get_new_face_id(self):
    return len(self._registry_face_ids)

  @staticmethod
  def _get_largest_face(face_boxes):
    """

    :param face_boxes: List of (top, right, bottom , left)
    :return:
    """
    face_areas = []
    for face_box in face_boxes:
      area = (face_box[1] - face_box[3]) * (face_box[2] - face_box[0])
      face_areas.append(area)
    face_areas = np.array(face_areas)
    largest_idx = np.argmax(face_areas)
    return face_boxes[largest_idx]
