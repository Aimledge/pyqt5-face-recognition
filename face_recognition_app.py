"""
Copyright (C) 2018, AIMLedge Pte, Ltd.
All rights reserved.

"""
import sys
from PyQt5.QtWidgets import QAction, QActionGroup, QMainWindow
from PyQt5.QtCore import QByteArray, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtMultimedia import QCamera
from gui.face_recognition_ui import Ui_FaceRecApp
from face_registration_view import \
  FaceRegistrationView, CreateRegistryView, DeleteRegistryView
from face_registry_view import FaceRegistryView
from aws_face_recognizer import AwsFaceRecognizer
from edge_face_recognizer import EdgeFaceRecognizer
from loggers import face_recognition_app_logger as \
  logger
import cv2

# Only OpenCV camera type is functional
CAMERA_TYPE = 'OpenCV' # or Qt


class FaceRecognitionAppUI(QMainWindow):
  def __init__(self, parent=None):
    QMainWindow.__init__(self, parent=parent)
    self.ui = Ui_FaceRecApp()

    self.ui.setupUi(self)
    self.camera = None
    self.running = False
    # self.face_recognizer = AwsFaceRecognizer()
    self.face_recognizer = EdgeFaceRecognizer()
    self.populate_face_registry_list()

    if CAMERA_TYPE == 'OpenCV':
      self.setup_opencv_camera()
    else:
      self.setup_camera()

    self.timer = QTimer(self, interval=5)
    self.timer.timeout.connect(self.process)

  def populate_face_registry_list(self):
    self.ui.faceRegistrySelect.blockSignals(True)
    for item in range(self.ui.faceRegistrySelect.count()):
      self.ui.faceRegistrySelect.removeItem(item)
    for registry in self.face_recognizer.list_face_registries():
      self.ui.faceRegistrySelect.addItem(registry)
    self.ui.faceRegistrySelect.blockSignals(False)

    if self.ui.faceRegistrySelect.currentText():
      self.set_current_registry(self.ui.faceRegistrySelect.currentText())

  def start(self):
    self.start_camera()
    self.timer.start()
    self.running = True

  def pause(self):
    pass

  def stop(self):
    self.timer.stop()
    logger.info('Stopping the app')
    self.running = False
    self.stop_camera()

  def register_faces(self):
    self.stop_camera()
    registration_dialog = FaceRegistrationView(parent=self,
                                               face_recognizer=self.face_recognizer)
    registration_dialog.exec_()
    logger.info('Done registering faces')
    self.start_camera()

  def create_registry(self):
    dialog = CreateRegistryView(parent=self, face_recognizer=self.face_recognizer)
    dialog.exec_()
    self.populate_face_registry_list()

  def delete_registry(self):
    dialog = DeleteRegistryView(parent=self, face_recognizer=self.face_recognizer)
    dialog.exec_()
    self.populate_face_registry_list()

  def set_current_registry(self, registry):
    assert registry is not None and registry != ''
    self.face_recognizer.set_active_face_registry(registry)

  def view_registry(self):
    self.stop_camera()
    registry_dialog = FaceRegistryView(parent=self,
                                       face_recognizer=self.face_recognizer)
    registry_dialog.exec_()
    self.start_camera()

  def setup_camera(self):
    camera_device = QByteArray()

    video_devices_group = QActionGroup(self)
    video_devices_group.setExclusive(True)

    for device in QCamera.availableDevices():
      description = QCamera.deviceDescription(device)
      video_device_action = QAction(description, video_devices_group)
      video_device_action.setCheckable(True)
      video_device_action.setData(device)

      if camera_device.isEmpty():
        camera_device = device
        video_device_action.setChecked(True)

      self.ui.menuDevices.addAction(video_device_action)
    if camera_device.isEmpty():
      self.camera = QCamera()
    else:
      self.camera = QCamera(camera_device)
    self.camera.setViewfinder(self.ui.cameraViewFinder)

  def setup_opencv_camera(self):
    if len(QCamera.availableDevices()) > 0:
      camera_addr = str(QCamera.availableDevices()[0])
      self.camera = cv2.VideoCapture(0)
      if self.camera.isOpened():
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        logger.info('Opened the camera {}'.format(camera_addr))
      else:
        logger.error('Failed to open the camera {}'.format(camera_addr))

  def stop_camera(self):
    if self.camera is None:
      return
    if CAMERA_TYPE == 'OpenCV':
      self.camera.release()
    else:
      self.camera.stop()

  def start_camera(self):
    if self.camera is None:
      return
    if CAMERA_TYPE == 'OpenCV':
      self.camera.open(0)
    else:
      self.camera.start()

  def update_frame(self):
    read, frame = self.camera.read()
    self.display_frame(frame)

  def display_frame(self, frame):
    if frame is None:
      return
    qformat = QImage.Format_Indexed8
    if len(frame.shape) == 3:
      if frame.shape[2] == 4:
        qformat = QImage.Format_RGBA8888
      else:
        qformat = QImage.Format_RGB888
    qt_image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0],
                      qformat)
    qt_image = qt_image.rgbSwapped()
    self.ui.cameraSurface.setPixmap(QPixmap.fromImage(qt_image))
    self.update()

  def process(self):
    assert self.camera is not None
    read, frame = self.camera.read()
    if not read:
      return
    recognition_results = self.face_recognizer.recognize_faces(frame)
    AwsFaceRecognizer.draw_face_recognitions(frame, recognition_results)
    self.display_frame(frame)

  def run_recognizer_with_opencv(self):
    self.camera.stop()
    cur_registry = self.ui.faceRegistrySelect.currentText()
    self.face_recognizer.set_active_face_registry(cur_registry)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not cap.isOpened():
      logger.warning('Unable to open the webcam')
      return

    cv2.namedWindow('Face recognizer', cv2.WINDOW_NORMAL)
    count = 0
    while True:
      read, frame = cap.read()
      if not read:
        logger.warning('Unable to read video frame')
        break
      recognition_results = self.face_recognizer.recognize_faces(frame)
      count += 1
      print('{}'.format(count), end='\r')
      sys.stdout.flush()

      AwsFaceRecognizer.draw_face_recognitions(frame, recognition_results)
      cv2.imshow('Face recognizer', frame)
      key = cv2.waitKey(5) & 255
      if key == 27:
        break
    cv2.destroyAllWindows()



