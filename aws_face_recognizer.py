"""
Copyright (C) 2018, AIMLedge Pte, Ltd.
All rights reserved.

"""
from face_recognizer import FaceRecognizer, logger
import boto3
from botocore.exceptions import *
from PIL import Image
import io
import cv2


def opencv_image_to_binary_image(image, format='JPEG'):
  """

  :param image: np.ndarray containing BGR image.
  :param format: Target encoding format.
  :return:
  """
  pil_image = Image.fromarray(image)
  stream = io.BytesIO()
  pil_image.save(stream, format=format)
  binary_image = stream.getvalue()
  return binary_image


class AwsFaceRecognizer(FaceRecognizer):

  def __init__(self):
    FaceRecognizer.__init__(self)
    logger.info('Creating AWS Rekognition client.')
    self._aws_client = boto3.client('rekognition')
    self._face_registries = self._get_aws_collections()
    self._active_face_registry = None

    # Holds current registry details
    self._registry_faces = []
    self._registry_face_names = []
    self._registry_face_ids = []

    self._detection_attributes = ['DEFAULT']
    self._detection_threshold = 80.0
    self._matching_threshold = 70.0
    # Enabling this will get more facial attributes such as age, gender.
    # self._detection_attributes = ['DEFAULT', 'ALL']
    logger.info('Created face recognizer.')
    logger.info('Existing face registries {}'.format(self._face_registries))

  def create_face_registry(self, registry_name):
    if registry_name in self._face_registries:
      logger.info('Face registry already present. Not creating again')
      return registry_name
    try:
      resp = self._aws_client.create_collection(CollectionId=registry_name)
      logger.debug('Collection ARN: ' + resp['CollectionArn'])
      logger.debug('Status code: ' + str(resp['StatusCode']))
      logger.info('Created face registry {}'.format(registry_name))
      self._face_registries.append(registry_name)
      return registry_name
    except Exception as e:
      logger.fatal(e)
      return None

  def delete_face_registry(self, registry_name):
    try:
      if registry_name not in self._face_registries:
        logger.warning('Looks like there is no such registry to delete.'
                       'Still trying with AWS'.format(registry_name))
      resp = self._aws_client.delete_collection(CollectionId=registry_name)
      if registry_name in self._face_registries:
        self._face_registries.remove(registry_name)
      status_code = resp['StatusCode']
    except ClientError as e:
      if e.response['Error']['Code'] == 'ResourceNotFoundException':
        logger.warning('Registry {} not found'.format(registry_name))
      else:
        logger.error('Error occured: {}'.format(e.response['Error']['Message']))
      status_code = e.response['ResponseMetadata']['HTTPStatusCode']
    logger.info('Delete face registry status: {}'.format(status_code))

  def get_active_face_registry(self):
    return self._active_face_registry

  def set_active_face_registry(self, registry_name):
    if registry_name not in self._face_registries:
      raise ValueError('Face registry not found {}'.format(registry_name))
    # Nothing to do
    logger.info('Setting active face registry to {}'.format(registry_name))
    if self._active_face_registry == registry_name:
      return
    # TODO: Load the face registry
    self._active_face_registry = registry_name
    return self._active_face_registry

  def list_face_registries(self):
    return self._face_registries

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
      image = cv2.imread(image)
    binary_image = opencv_image_to_binary_image(image)
    resp = self._aws_client.index_faces(CollectionId=registry_name,
                                        Image={'Bytes': binary_image},
                                        ExternalImageId=name,
                                        MaxFaces=1,
                                        QualityFilter="AUTO",
                                        DetectionAttributes=['ALL'])
    logger.info('Faces registered:')
    for face_record in resp['FaceRecords']:
      logger.info('Face ID: ' + face_record['Face']['FaceId'])
      logger.info('Location: {}'.format(face_record['Face']['BoundingBox']))
      logger.info('Face name: ' + face_record['Face']['ExternalImageId'])
      if registry_name == self._active_face_registry:
        box = AwsFaceRecognizer._decode_aws_bounding_box(
          face_record['Face']['BoundingBox'], image.shape[1], image.shape[0])
        crop = image[box[1]:box[3], box[0]:box[2], :]
        self._registry_face_ids.append(face_record['Face']['FaceId'])
        self._registry_face_names.append(face_record['Face']['ExternalImageId'])
        self._registry_faces.append(crop)

    logger.info('Faces not registered:')
    for unindexed_face in resp['UnindexedFaces']:
      logger.info('Location: {}'.format(
        unindexed_face['FaceDetail']['BoundingBox']))
      logger.info('Reasons:')
      for reason in unindexed_face['Reasons']:
        logger.info('  ' + reason)

  def recognize_faces(self, image):
    # First, detect faces in the image
    face_boxes = self._detect_faces(image)
    # Crop and search for each face in the active registry
    rec_result = []
    for face_box in face_boxes:
      box = face_box['box']
      face_crop = image[box[1]:box[3], box[0]:box[2], :]
      bin_face_crop = opencv_image_to_binary_image(face_crop)
      try:
        resp = self._aws_client.search_faces_by_image(
          CollectionId=self._active_face_registry,
          Image={'Bytes': bin_face_crop},
          MaxFaces=1,
          FaceMatchThreshold=self._matching_threshold
        )
        if len(resp['FaceMatches']) >= 1:
          match = resp['FaceMatches'][0]
          rec_result.append({
            'face_id': match['Face']['FaceId'],
            'face_name': match['Face']['ExternalImageId'],
            'recognition_score': match['Similarity'],
            'box': box,
            'detection_score': face_box['detection_score']
          })
        else:
          rec_result.append({
            'face_id': None,
            'face_name': 'Unknown',
            'recognition_score': None,
            'box': box,
            'detection_score': face_box['detection_score']
          })
      except Exception as e:
        logger.warning('Some error occured when searching for the face. '
                       'Skipping this face. {}'.format(e))
        rec_result.append({
          'face_id': None,
          'face_name': 'Unknown',
          'recognition_score': None,
          'box': box,
          'detection_score': face_box['detection_score']
        })
    return rec_result

  def deregister_face(self, registry_name, face_id):
    try:
      resp = self._aws_client.delete_faces(CollectionId=registry_name,
                                           FaceIds=[face_id]
                                           )
      assert len(resp['DeletedFaces']) == 1
      deleted_face_id = resp['DeletedFaces'][0]
      deleted_face_name = None
      logger.warning('Deleted face: {}'.format(deleted_face_id))
      if registry_name == self._active_face_registry:
        idx = self._registry_face_ids.index(face_id)
        deleted_face_name = self._registry_face_names[idx]
        del self._registry_face_ids[idx]
        del self._registry_face_names[idx]
        del self._registry_faces[idx]
      return deleted_face_id, deleted_face_name
    except Exception as e:
      logger.warning('Error occured. Could not de-register face.')
      logger.warning(e)
      return None, None

  def get_face_name(self, registry_name, face_id):
    if registry_name != self._active_face_registry:
      raise ValueError('Cannot get face name from inactive registry')
    if face_id in self._registry_face_ids:
      return self._registry_face_names[self._registry_face_ids.index(face_id)]
    else:
      return None

  def _get_aws_collections(self):
    all_collections = []
    resp = self._aws_client.list_collections(MaxResults=2)
    while True:
      collections = resp['CollectionIds']

      for collection in collections:
        all_collections.append(collection)
      if 'NextToken' in resp:
        resp = self._aws_client.list_collections(NextToken=resp['NextToken'],
                                                 MaxResults=2)
      else:
        break
    return all_collections

  def _detect_faces(self, image):
    binary_image = opencv_image_to_binary_image(image)
    face_boxes = []
    try:
      resp = self._aws_client.detect_faces(
        Image={'Bytes': binary_image},
        Attributes=self._detection_attributes
      )
      for face_detail in resp['FaceDetails']:
        if face_detail['Confidence'] >= self._detection_threshold:
          face_box = AwsFaceRecognizer._decode_aws_bounding_box(
            face_detail['BoundingBox'], image.shape[1], image.shape[0])
          score = face_detail['Confidence']
          face_boxes.append({'detection_score': score, 'box': face_box})
    except Exception as e:
      logger.warning('Error occured when detecting faces. {}'.format(e))
    return face_boxes

  @staticmethod
  def _decode_aws_bounding_box(aws_bouding_box, image_width,
                               image_height):
    """

    :param aws_bouding_box:
    :param image_width:
    :param image_height:
    :return:
    """
    xmin = max(0, int(image_width * aws_bouding_box['Left']))
    ymin = max(0, int((image_height * aws_bouding_box['Top'])))
    xmax = min(image_width-1, xmin + int(image_width * aws_bouding_box['Width']))
    ymax = min(image_height-1, ymin + int(image_height * aws_bouding_box['Height']))
    return [xmin, ymin, xmax, ymax]
