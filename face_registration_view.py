"""
Copyright (C) 2018, AIMLedge Pte, Ltd.
All rights reserved.

"""
import os
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture
from gui.face_registration_view_ui import Ui_FaceRegistrationUI
from gui.create_registry_ui import Ui_CreateRegistry
from gui.delete_registry_ui import Ui_DeleteRegistry
from loggers import face_recognition_app_logger as logger


class CreateRegistryView(QDialog):
  def __init__(self, parent=None, face_recognizer=None):
    QDialog.__init__(self, parent=parent)
    self.msg_box = QMessageBox()
    self.ui = Ui_CreateRegistry()
    self.ui.setupUi(self)
    self.registry_name = None
    self.face_recognizer = face_recognizer

  def create_registry(self):
    name = self.ui.registryNameInput.text()
    if name == '':
      self.msg_box.setIcon(QMessageBox.Critical)
      self.msg_box.warning(self, 'Error', 'Album name cannot be empty!')
      return

    name = name.replace(' ', '_')
    confirm_msg = 'Are you sure that you want to create album {}?'.format(name)
    reply = QMessageBox.question(self, 'Create album', confirm_msg,
                                 QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
      print('Creating registry {}'.format(name))
      registry = self.face_recognizer.create_face_registry(name)
      if registry is not None:
        logger.info('Successfully created face registry {}'.format(registry))
    self.close()

  def set_registry_name(self, name):
    self.registry_name = name


class DeleteRegistryView(QDialog):
  def __init__(self, parent=None, face_recognizer=None):
    QDialog.__init__(self, parent=parent)
    self.face_recognizer = face_recognizer

    self.ui = Ui_DeleteRegistry()
    self.ui.setupUi(self)
    for registry in self.face_recognizer.list_face_registries():
      self.ui.faceRegistryBox.addItem(registry)
    if len(self.face_recognizer.list_face_registries()) == 0:
      self.ui.deleteButton.setEnabled(False)

  def delete_registry(self):
    current_registry = self.ui.faceRegistryBox.currentText()
    confirm_msg = 'Are you sure that you want to delete {}'.format(
      current_registry)
    reply = QMessageBox.question(self, 'Delete album', confirm_msg,
                                 QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
      logger.warning('Deleting {}'.format(current_registry))
      self.face_recognizer.delete_face_registry(current_registry)
      self.close()


class FaceRegistrationView(QDialog):
  def __init__(self, parent=None, face_recognizer=None):
    QDialog.__init__(self, parent=parent)
    self.face_recognizer = face_recognizer
    self.ui = Ui_FaceRegistrationUI()

    self.ui.setupUi(self)

    # Add existing face albums to the combobox
    # FIXME: need to get this list from the face recognizer
    for registry in self.face_recognizer.list_face_registries():
      self.ui.registryNameSelect.addItem(registry)

    self.ui.retakeButton.setEnabled(False)
    self.cur_face_name = None
    self.cur_face_registry = self.ui.registryNameSelect.currentText()
    self.camera = None
    self.image_capture = None
    self.cur_saved_image_path = None
    self.setup_camera()

  def setup_camera(self):
    camera_device = QByteArray()

    for device in QCamera.availableDevices():
      if camera_device.isEmpty():
        camera_device = device
    if camera_device.isEmpty():
      self.camera = QCamera()
    else:
      self.camera = QCamera(camera_device)

    self.image_capture = QCameraImageCapture(self.camera)
    self.image_capture.readyForCaptureChanged.connect(self.ready_for_capture)
    self.image_capture.imageCaptured.connect(self.process_captured_image)
    self.image_capture.imageSaved.connect(self.image_saved)

    self.camera.setViewfinder(self.ui.viewFinder)
    self.camera.start()

  def ready_for_capture(self, ready):
    self.ui.captureButton.setEnabled(ready)

  def process_captured_image(self, request_id, image):
    scaled_image = image.scaled(self.ui.viewFinder.size(),
                                Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.ui.picturePreview.setPixmap(QPixmap.fromImage(scaled_image))
    self.show_captured_image()

  def image_saved(self, id, file_path):
    self.cur_saved_image_path = file_path
    logger.info('Image saved at {}'.format(file_path))

  def handle_face_name(self, name):
    self.cur_face_name = name

  def register_face(self):
    name = self.ui.nameInput.text()
    if name == '':
      msg_box = QMessageBox()
      msg_box.setIcon(QMessageBox.Critical)
      msg_box.warning(self, 'Error', 'Person name cannot be empty!')
      return

    confirm_msg = 'Register face of {:s} into {:s}?'.format(name,
                                                           self.cur_face_registry)
    reply = QMessageBox.question(self, 'Register face', confirm_msg,
                                   QMessageBox.No, QMessageBox.Yes)
    if reply == QMessageBox.Yes:
      logger.info('Registering {:s}'.format(name))
      try:
        self.face_recognizer.register_face(self.cur_face_registry,
                                           self.cur_saved_image_path, name)
        self.parent().ui.statusbar.showMessage(
          'Successfully registered the face', 2000)

      except Exception as e:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.warning(self, 'Error', str(e))
      # Clean up the captured image and show the video stream again
      self.ui.nameInput.clear()
      # self.ui.nameInput.setText('')
      self.retake_picture()
    else:
      pass

  def retake_picture(self):

    self.delete_current_picture()
    self.ui.captureButton.setEnabled(True)
    self.ui.retakeButton.setEnabled(False)
    self.show_video_stream()

  def capture_picture(self):
    self.image_capture.capture()
    self.ui.captureButton.setEnabled(False)
    self.ui.retakeButton.setEnabled(True)

  def show_captured_image(self):
    self.ui.stackedWidget.setCurrentIndex(1)

  def show_video_stream(self):
    self.ui.stackedWidget.setCurrentIndex(0)

  def set_current_face_registry(self, registry_name):
    self.cur_face_registry = registry_name

  def closeEvent(self, event):
    self.camera.stop()
    self.delete_current_picture()

  def accept(self):
    self.camera.stop()
    self.delete_current_picture()
    QDialog.reject(self)

  def reject(self):
    self.camera.stop()
    logger.info('Cleaning up captured images...')
    self.delete_current_picture()
    QDialog.reject(self)

  def delete_current_picture(self):
    if self.cur_saved_image_path is not None:
      if os.path.exists(self.cur_saved_image_path):
        os.remove(self.cur_saved_image_path)
        logger.info('Deleted {}'.format(self.cur_saved_image_path))
      self.cur_saved_image_path = None


if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)
  dialog = FaceRegistrationView()
  dialog.show()
  sys.exit(app.exec_())
